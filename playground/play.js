import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import { html as toReactElement } from "satori-html";
import fsPromises from "fs/promises";
import { writeFile } from "fs";

const fontFile = await fsPromises.readFile("Poppins-Bold.ttf");
const font = fontFile;

// Will come after jinja template has been rendered
const template = (
  prefix,
  title,
  subtitle
) => `<div style="color: white; height: 100vh; width: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column">    
    <h1 style="font-size: 40px">${prefix}${title}</h1>
    <h2 style="font-size: 20px">${subtitle}</h2>
</div>`;

const width = 1200;

const content = template("prefix", "title", "subtitle");

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

writeFile("./out.png", pngBuffer, () => {})
