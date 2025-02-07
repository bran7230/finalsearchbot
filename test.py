import requests
from bs4 import BeautifulSoup
from googlesearch import search

while True:
    # Get user input for a search query
    user_input = input("Enter your search query: ")

    # Perform a Google search based on the user input
    print("\nPerforming Google search...")
    search_results = list(search(user_input))  
    if search_results:
        print(f"Found {len(search_results)} results. Starting scraping...")
    else:
        print("No search results found.")
        continue

    # Open the file once for writing all website content
    with open("scraped_content.txt", "w", encoding="utf-8") as file:
        for idx, target_url in enumerate(search_results, start=1):
            print(f"Scraping content from result {idx}: {target_url}")
            
            try:
                response = requests.get(target_url)
                if response.status_code == 200:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Extract all paragraphs
                    paragraphs = soup.find_all('p')

                    # Write content for each website in a separate section
                    file.write(f"---START OF CONTENT FROM WEBSITE {idx} ---\n\n")
                    file.write(f"Source URL: {target_url}\n\n")
                    for para in paragraphs:
                        text = para.get_text(strip=True)  # Get clean text from paragraph
                        if text:  # Write only non-empty paragraphs
                            file.write(text + "\n\n\n")
                    file.write("\n--- END OF CONTENT FROM WEBSITE---\n\n\n\n")
                else:
                    file.write(f"Failed to fetch content from {target_url}\n")
                    print(f"Failed to fetch content from {target_url}")
            except Exception as e:
                file.write(f"Error scraping {target_url}: {str(e)}\n")
                print(f"Error scraping {target_url}: {str(e)}")

    print(f"Content saved to 'scraped_content.txt'.")
    
