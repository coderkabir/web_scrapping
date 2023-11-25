import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_blog_data(url):
    # Set headers to mimic a request from a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize lists to store data
        titles = []
        dates = []
        image_urls = []

        # Find all blog posts on the page
        blog_posts = soup.find_all('div', class_='wrap')  # Update the class name based on the actual structure

        # Loop through each blog post and extract information
        for post in blog_posts:
            # Extract blog title
            title = post.find('div', class_='content').find('h6').find('a').text.strip()
            titles.append(title)
            
            # Extract blog date
            date_element = post.find('div', class_='bd-item').find('span')  # Find the first span within the bd-item div
            date = date_element.text.strip() if date_element else "N/A"
            dates.append(date)

            # Extract blog image URL
            wrap_div = post.find('div', class_='wrap')  # Update the class name based on the actual structure
            img_div = wrap_div.find('div', class_='img') if wrap_div else None
            a_tag = img_div.find('a') if img_div else None
            img_element = a_tag.find('img') if a_tag else None
            image_url = img_element['src'] if img_element else "N/A"
            image_urls.append(image_url)

            # Introduce a delay to avoid being blocked
            time.sleep(2)  # Sleep for 2 seconds (adjust as needed)

        # Create a DataFrame to store the data
        data = {'Blog Title': title, 'Blog Date': dates, 'Blog Image URL': image_urls}
        df = pd.DataFrame(data)

        # Save the data to a CSV file
        df.to_csv('blog_data.csv', index=False)
        print("Data has been successfully scraped and saved to 'blog_data.csv'.")

    else:
        print(f"Error: Unable to retrieve data from the URL. Status code: {response.status_code}")

if __name__ == "__main__":
    url = "https://rategain.com/blog"
    scrape_blog_data(url)
