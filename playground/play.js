import satori from "satori";
import { writeFile } from "fs";
import fsPromises from "fs/promises";
import { Resvg } from "@resvg/resvg-js";
import { html as toReactElement } from "satori-html";

const output_path = process.argv[2];
const content = process.argv[3];

const fontFile = await fsPromises.readFile("Poppins-Bold.ttf");
const font = fontFile;

const width = 1200;

const svg = await satori(toReactElement(content), {
  width,
  height: 630,
  fonts: [
    {
      name: "Poppins",
      data: font,
      style: "bold",
    },
  ],
});

const resvg = new Resvg(svg, {
  fitTo: {
    mode: "width",
    value: width,
  },
});

const pngData = resvg.render();
const pngBuffer = pngData.asPng();

writeFile(output_path, pngBuffer, () => {})
