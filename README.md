# Random Geekery Blog via Astro

- an experiment building <https://randomgeekery.org>
- primarily a blog
- multiple sections
- includes non-blog content

The material in this repo is licensed under a Creative Commons license. See
[LICENSE.md][./LICENSE.md] for those details.

## Tools

- uses [Astro][]
- driving it with [Yarn][] — "classic" version apparently
- non-Astro components written with [Vue][]

[Astro]: https://astro.build
[Yarn]: https://yarnpkg.com
[Vue]: https://vuejs.org

## MVP Goals

Sort of in priority order, but probably won't be completed in priority order.

- [x] all markdown sources get loaded
- [ ] meta pages to list bundle content
- [ ] images get loaded
    - [ ] store originals in `assets/img` with subpath matching endpoint
    - [ ] transform assets
        - [ ] write results to `src/` I think
        - [ ] max size
        - [ ] responsive sizes
        - [ ] format (`.webp`)
- [ ] Components
    - [ ] `<Figure />`
    - [ ] `<Note />`
    - [ ] `<Tldr />`
        - alternately, use frontmatter
- [ ] RSS Feeds
    - [ ] `post` feed
    - [ ] `note` feed
- [ ] URL aliases
    - just target `.htaccess`; no need to invent or use redirect files
- [ ] URLs of original Hugo site are respected
- [ ] tag list

## Side Quests

- [ ] Nice style
- [ ] IndieWeb integration

## Project Structure

Project structure builds on the standard Astro layout:

```
bsh ❯ tree . -I 'node_modules|dist' -L 3
.
├── README.md
├── astro.config.mjs
├── package.json
├── public
│   ├── favicon.ico
│   └── robots.txt
├── sandbox.config.json
├── src
│   ├── components
│   │   ├── AstroVersion.astro
│   │   ├── Card.astro
│   │   ├── DateStamp.astro
│   │   ├── Masthead.astro
│   │   ├── NoteCard.astro
│   │   ├── PageMeta.astro
│   │   ├── PostCard.astro
│   │   ├── SiteFooter.astro
│   │   └── SiteMenu.astro
│   ├── layouts
│   │   ├── Article.astro
│   │   ├── BaseLayout.astro
│   │   ├── MarkdownPage.astro
│   │   └── PublishedArticle.astro
│   ├── pages
│   │   ├── about
│   │   ├── config
│   │   ├── draft
│   │   ├── follow
│   │   ├── index.astro
│   │   ├── note
│   │   ├── now
│   │   └── post
│   └── styles
│       └── global.css
├── tsconfig.json
└── yarn.lock
```

## How I'm using the content formats

- `.astro` files are for master and meta content; like a Hugo `_index.md` file
- `.md` files are for — you know — *content*; blog posts etc

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command       | Action                                       |
|:------------  |:-------------------------------------------- |
| `yarn`        | Installs dependencies                        |
| `yarn dev`    | Starts local dev server at `localhost:3000`  |
| `npm build`   | Build your production site to `./dist/`      |
| `npm preview` | Preview your build locally, before deploying |

## Resources

- [Astro docs][]

[Astro docs]: https://github.com/withastro/astro
