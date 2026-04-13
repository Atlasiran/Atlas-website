import { readdirSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function getAllOPPaths() {
    const postsDirectory = path.join(__dirname, '..', 'content', 'org-pages');
    try {
        const files = readdirSync(postsDirectory);
        const opPaths = files
            .filter(file => file.endsWith('.md') && file.length > 3)
            .map(file => `/op/${file.replace('.md', '')}`);
        return opPaths;
    } catch (err) {
        console.error('Error reading directory:', err);
        throw err;
    }
}

export function getAllBlogPaths() {
    const postsDirectory = path.join(__dirname, '..', 'content', 'posts');
    try {
        const files = readdirSync(postsDirectory);
        return files
            .filter(file => file.endsWith('.md') && file.length > 3)
            .map(file => `/blog/${file.replace('.md', '')}`);
    } catch (err) {
        console.error('Error reading directory:', err);
        throw err;
    }
}