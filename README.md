<p align="center">
  <a href="https://github.com/NagariaHussain/frappe_dynamic_og">
    <img src="./.github/images/fdog_logo.png" width="380" />
  </a>
</p>
<h1 style="font-size: 24px" align="center">Dynamically Generate OG Images in your Frappe sites</h1>

<p align="center">

![Server Tests](https://github.com/NagariaHussain/frappe_dynamic_og/actions/workflows/ci.yml/badge.svg)
![e2e Tests](https://github.com/NagariaHussain/frappe_dynamic_og/actions/workflows/playwright.yml/badge.svg)

</p>

## 📋 Features

- [x] Define DocType-wise templates for generating images
- [x] "Live" Preview in OG Image Template
- [x] Automatically re-generates images on document changes
- [x] Automatically attach the generated image to a particular field in the document
- [x] Full Inter Font Family supported in the image HTML template
- [x] Automatically delete older image files
- [x] Up to 1920x1080 images (for now.)
- [x] Tests! (yup, I consider it a pretty good feature 😉)
- [x] Update existing OG images on documents in bulk from OG Template form/API

## 📀 Installation

Make sure you have Frappe bench installed. You can install this app on your Frappe site by running:

```bash
bench get-app https://github.com/NagariaHussain/frappe_dynamic_og
bench --site my_site.localhost install-app frappe_dynamic_og
```

This app requires **Node >= 16** and **Frappe Version >= 14**.

## 👩🏼‍💻 Usage

The most important DocType in this app is **OG Image Template**. When you want to generate OG images (well, you can use the generated image for anything you want) for a given DocType, just create a new **OG Image Template** document. For example, if I want to generate an OG image for the `ToDo` DocType, I will set the **For Doctype** field in the form to `ToDo`:

![Screenshot of OG Image Template For ToDo](https://frappecloud.com/files/sample_todo_og_image_template_form_view.png)

The Template HTML field takes a `jinja` template. The document is available in the content as `doc`, so, in the above template `{{ doc.status }}` will be replaced by the status of the `ToDo` document. We are also using the `color` field of `ToDo` as background color of the generated image.

> Please note that when a `div` has more than 1 child, you have to explicitly specify `display:flex;` on it. Please check [satori's documentation](https://github.com/vercel/satori) to learn what HTML element and style properties are supported.

**The Result:**

https://user-images.githubusercontent.com/34810212/206919225-66016d1a-562c-4fa4-b778-315803ee70ff.mp4

### Attach To Image Field

If you want to attach the generated image to a `Attach Image` type field on the document, you can easily do so by checking the "Attach to Image Field?" checkbox and provide the name for the attach image field in the doctype. For instance, if I want to generate an image for the `User` doctype and attach the image to the **Banner Image** (`banner_image`) field, I only need to do this:

![Screenshot of OG Image Template For User](https://frappecloud.com/files/sample_user_og_image_template_form_view.png)

**The Result:**

https://user-images.githubusercontent.com/34810212/206919330-63ecd171-e645-4439-aa06-f9d3bf539073.mp4

### Preview Image

You can preview your template using the **Generate Preview** button in the `OG Image Template` doctype:

![Template Preview](https://user-images.githubusercontent.com/34810212/207047971-6df567f9-eb2d-4e30-babb-adab4fed994b.png)

You can optionally enable **Debug Mode** which shows *bounding boxes* around your elements.

## 🌄 Examples

### Default Template

The below is the default template set when you create a new **OG Image Template** document.

Template HTML:

```html
<div style="display: flex; background-color: #fff; color: #313B44; height: 100vh; width: 100%; align-items: center; justify-content: center; flex-direction: column"> 
    <span style="font-size: 60px; font-style: semibold; color: #74808B; text-transform: uppercase;">{{ doc.doctype }}</span>
    <h1 style="font-size: 120px; font-style: bold;">{{ doc.get_title() }}</h1>
    <img style="position: absolute;height: 40px;left: 40px;top: 40px;" src="https://frappeframework.com/files/frappeframework-logo2a3e81.png" />
</div>
```

Output:

![Default Template](https://user-images.githubusercontent.com/34810212/207801893-fa6f7146-b10d-4efc-b628-d1db29f9dfc1.png)

If you use the above template for the **Web Form** DocType, you will get the below image generated for a web form with title 'Job Opportunity':

![Job Opportunity Web Form OG Image](https://user-images.githubusercontent.com/34810212/207803551-7cd2805e-016e-4674-a03c-a0e5a206cbf5.png)

More examples soon.

## 📍 Planned Features 

- [ ] Delete og image files on trash of document
- [ ] Configurable fonts via Google Fonts
- [ ] Use something like [this](https://github.com/jonkemp/inline-css) to support style tags instead of manual inline CSS
- [ ] Only update OG image based on fields used in HTML template
- [ ] API to generate OG images dynamically
- [ ] Queueing of image generation

#### License

[MIT](./LICENSE.txt)