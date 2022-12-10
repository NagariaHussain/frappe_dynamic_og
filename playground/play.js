import satori from "satori";
import fsPromises from "fs/promises";
import { Resvg } from "@resvg/resvg-js";
import { html as toReactElement } from "satori-html";

const content = process.argv[2];

// TODO: Can come from fetch if custom google font
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

// Std Out, maybe let python handle the saving to file?
process.stdout.write(pngBuffer)