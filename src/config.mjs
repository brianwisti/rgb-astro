import path from "path";

import fg from "fast-glob";
import matter from "gray-matter";

// NOTES:
//  - requires a restart when content files are changed
//  - assumes POSIX path separators
//
// if I put this in src/config.mjs:
//
//  node_modules/@small-tech/jsdb/lib/JSTable.js:17:23: \
//    error: Could not resolve "fs/promises"            \
//    (use "platform: 'node'" when building for node)

const loadContentSummaries = async () => {
    console.log("Loading content summaries");
    const datedSections = ["post", "note"];
    const currentDir = process.cwd();
    // at home it's /home/random/Sites/astro-fast
    console.log(`currentDir: ${currentDir}`);
    const contentRoot = path.join(currentDir, "src/pages");
    const contentGlob = path.join(contentRoot, "**/*.md");
    console.log(`contentGlob: ${contentGlob}`);

    const contentPaths = await fg(contentGlob);

    const contentEntries = contentPaths.map(contentPath => {
        const file = matter.read(contentPath);
        const { date, title, tags } = file.data;

        // extract href
        let href = contentPath.replace(contentRoot, '');

        if (path.basename(href) == "index.md") {
            href = path.dirname(href);
        }
        else {
            href = href.replace(".md", "");
        }

        // extract section and year for organization
        const pathParts = href.split("/");
        const section = pathParts[1];
        const year = (datedSections.includes(section)) ? pathParts[2] : "0000";

        // extract description for cards
        let cardContent = file.data.description;
        if (cardContent === undefined) {
            // TODO: truncate to first useful paragraph
            cardContent = file.content;
        }

        return {
            contentPath,
            href,
            section,
            year,
            date,
            title,
            tags,
            cardContent,
        }
    });
    return contentEntries;
};

const contentSummaries = await loadContentSummaries();

export default contentSummaries;