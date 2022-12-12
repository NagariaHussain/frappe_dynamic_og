import path from "path";
import satori from "satori";
import fsPromises from "fs/promises";
import { Resvg } from "@resvg/resvg-js";
import { html as toReactElement } from "satori-html";

const content = process.argv[2];

// Debug Mode (bounding boxes)
let isDebugModeOn = false;
if (process.argv.length === 4 && process.argv[3] === "--debug") {
  isDebugModeOn = true;
}

// Load Inter Font Files
const inter_font_path = "fonts/inter/";
const files = await fsPromises.readdir(inter_font_path);
const fonts = [];

for (let file of files) {
  let font = await fsPromises.readFile(path.join(inter_font_path, file));
  fonts.push({
    name: "Inter",
    data: font,
    style: file.split("-")[1].split(".")[0].toLowerCase(),
  });
}

const width = 1920;
const height = 1080;

const svg = await satori(toReactElement(content), {
  width,
  height,
  fonts,
  debug: isDebugModeOn,
});

const resvg = new Resvg(svg, {
  fitTo: {
    mode: "width",
    value: width,
  },
});

const pngData = resvg.render();
const pngBuffer = pngData.asPng();

// Std Out, maybe let python handle the saving to file?
process.stdout.write(pngBuffer);
