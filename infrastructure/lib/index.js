import WebscraperStack from "./WebscraperStack";

// Add stacks
export default function main(app) {
  new WebscraperStack(app, "webscraper");
}