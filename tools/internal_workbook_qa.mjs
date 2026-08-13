import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const [inputPath, outputDir] = process.argv.slice(2);
if (!inputPath || !outputDir) {
  throw new Error("usage: node internal_workbook_qa.mjs INPUT.xlsx OUTPUT_DIR");
}

await fs.mkdir(outputDir, { recursive: true });
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));

const overview = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 12000,
  tableMaxRows: 6,
  tableMaxCols: 8,
  tableMaxCellChars: 100,
});
await fs.writeFile(`${outputDir}/overview.ndjson`, overview.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
await fs.writeFile(`${outputDir}/formula-errors.ndjson`, errors.ndjson);

const sheets = workbook.worksheets.items;
const manifest = [];
for (let index = 0; index < sheets.length; index += 1) {
  const sheet = sheets[index];
  const file = `sheet-${String(index + 1).padStart(2, "0")}.png`;
  const preview = await workbook.render({
    sheetName: sheet.name,
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(`${outputDir}/${file}`, new Uint8Array(await preview.arrayBuffer()));
  manifest.push({ index: index + 1, name: sheet.name, file });
}
await fs.writeFile(`${outputDir}/render-manifest.json`, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({ sheets: manifest.length, outputDir }));
