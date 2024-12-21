from src.MarkdownContentWriter import MarkdownContentWriter

async def main():
    # url_content = await crawler.run("https://en.wikipedia.org/wiki/Python_(programming_language)")
    file_path = "C:\\Users\\niche\\ai-home-lab-docker-compose\\agentic\\logs\\crawler\\2024-12-20\\firecraw-2024-12-20-httpsenwikipediaorgwikiPythonprogramminglanguage.md"
    with open(file_path, "r", encoding="utf-8") as file:
        url_content = file.read()

    async for chunk in MarkdownContentWriter.stream(context=url_content):
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
