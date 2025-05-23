import requests
import os

# Base URL of your API
BASE_URL = "http://localhost:8080"

def test_movie_upload(image_path, title, description):
    """Test the movie upload endpoint with an image file"""
    url = f"{BASE_URL}/api/v1/movies"
    
    # Prepare the data
    files = {
        'poster': open(image_path, 'rb')
    }
    data = {
        'title': title,
        'description': description
    }
    
    try:
        # Make the POST request
        response = requests.post(url, files=files, data=data)
        
        # Print the response
        print(f"\nTesting with image: {os.path.basename(image_path)}")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)  # Print raw response text
        try:
            print("Response JSON:", response.json())
        except:
            print("Could not parse response as JSON")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e)}")
    finally:
        # Close the file
        files['poster'].close()

if __name__ == "__main__":
    # Test with your image files
    test_movie_upload(
        "uploads/barbie.jpg",
        "Barbie",
        "Barbie suffers a crisis that leads her to question her world and her existence."
    )
    
    test_movie_upload(
        "uploads/final destination.jpg",
        "Final Destination",
        "After a teenager has a terrifying vision of him and his friends dying in a plane crash, he prevents the accident only to have Death hunt them down, one by one."
    )
    
    test_movie_upload(
        "uploads/end game.jpg",
        "Avengers: Endgame",
        "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe."
    ) 