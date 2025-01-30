import requests

from typing import List
from termcolor import colored

def search_for_stock_videos(query: str, api_key: str, it: int, min_dur: int) -> List[str]:
    """
    Searches for stock videos based on a query.

    Args:
        query (str): The query to search for.
        api_key (str): The API key to use.

    Returns:
        List[str]: A list of stock videos.
    """
    
    # Build headers
    headers = {
        "Authorization": api_key
    }

    # Build URL
    qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={it}"

    # Send the request
    r = requests.get(qurl, headers=headers)

    # Parse the response
    response = r.json()

    # Parse each video
    raw_urls = []
    video_url = []
    video_res = 0
    try:
        # loop through each video in the result
        for i in range(it):
            #check if video has desired minimum duration
            if response["videos"][i]["duration"] < min_dur:
                continue
            raw_urls = response["videos"][i]["video_files"]
            temp_video_url = ""
            
            # loop through each url to determine the best quality
            for video in raw_urls:
                # Check if video has a valid download link
                if ".com/video-files" in video["link"]:
                    # Only save the URL with the largest resolution
                    if (video["width"]*video["height"]) > video_res:
                        temp_video_url = video["link"]
                        video_res = video["width"]*video["height"]
                        
            # add the url to the return list if it's not empty
            if temp_video_url != "":
                video_url.append(temp_video_url)
                
    except Exception as e:
        print(colored("[-] No Videos found.", "red"))
        print(colored(e, "red"))

    # Let user know
    print(colored(f"\t=> \"{query}\" found {len(video_url)} Videos", "cyan"))

    # Return the video url
    return video_url




def search_company(query: str, api_key: str) -> List[str]:

    # TAVILY_API_KEY
    # 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

    # We can take the company name then scrape the lightly company website
    # once we get the company scraped data
    # Summarize the company
    # then return the summary
    # Store  Summary in database
    """
    Searches for companies based on a query.
    
 
    Args:
        query (str): The query to search for.
        api_key (str): The API key to use.

    Returns:
        List[str]: A list of companies.
    """

    # We can take the company name then scrape the lightly company website
    # once we get the company scraped data
    # Summarize the company
    # then return the summary
    # Store  Summary in database

    # First, let's make a GET request to the company API endpoint
    url = f"https://api.example.com/companies/{query}"
    
    # Send the request
    r = requests.get(url)

    # Parse the response
    response = r.json()

    # Get the company data from the response
    company_data = response["company"]

    # Summarize the company data
    summary = f"Company Name: {company_data['name']}\n"
    summary += f"Description: {company_data['description']}\n"
    summary += f"Founded: {company_data['founded']}"

    # Return the summary
    return [summary]
