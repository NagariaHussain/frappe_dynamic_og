<p align="center">
  <a href="https://github.com/NagariaHussain/frappe_dynamic_og">
    <img src="./.github/images/fdog_logo.png" width="380" />
  </a>
</p>
<h1 style="font-size: 24px" align="center">Dynamically Generate OG Images in your Frappe sites</h1>

## Features 📋

- [x] Define DocType-wise templates for generating images
- [x] Automatically re-generates images on document changes
- [x] Automatically attach the generated image to a particular field in the document
- [x] Full Inter Font Family supported in the image HTML template
- [x] Automatically delete older image files
- [x] Tests! (yup, I consider it a pretty good feature 😉)

## Installation 📀

Make sure you have Frappe bench installed. You can install this app on your Frappe site by running:

```bash
bench get-app https://github.com/NagariaHussain/frappe_dynamic_og
bench --site my_site.localhost install-app frappe_dynamic_og
```

This app requires Node >= 16 and Frappe Version >= 14.

## Usage

## Planned Features 📍

- [ ] Delete og image files on trash of document
- [ ] Embed images in OG Images
- [ ] Configurable fonts via Google Fonts
- [ ] Update existing OG images on documents in bulk from OG Template form/API
- [ ] Use something like [this](https://github.com/jonkemp/inline-css) to support style tags instead of manual inline CSS
- [ ] Only update OG image based on fields used in HTML template
- [ ] Live Preview while writing template
- [ ] API to generate OG images dynamically

#### License

[MIT](./LICENCE.txt)