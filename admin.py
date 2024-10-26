import streamlit as st
import pandas as pd
from datetime import datetime

# Function to add a book to the library database
def add_book(book_data):
    try:
        # Try reading existing data from the Excel file
        df = pd.read_excel('library_database.xlsx')
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        df = pd.DataFrame(columns=['Book Name', 'Author', 'Genre', 'Publication', 'Date of Publication', 'ISBN', 'Rack Number', 'Floor'])
    
    # Append new book data to the DataFrame
    df = pd.concat([df, book_data], ignore_index=True)
    
    # Write the DataFrame back to the Excel file
    df.to_excel('library_database.xlsx', index=False)

# Function to update book details in the library database
def update_book(old_book_name, updated_data):
    df = pd.read_excel('library_database.xlsx')
    index = df.index[df['Book Name'] == old_book_name].tolist()[0]
    df.loc[index] = updated_data
    df.to_excel('library_database.xlsx', index=False)

# Function to search for a book in the library database
def search_book(search_term):
    df = pd.read_excel('library_database.xlsx')
    result = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
    return result

# Main function to run the Streamlit app
def main():
    st.title('Library Management System')
    
    # Search book section
    st.subheader('Search for a Book')
    search_term = st.text_input('Enter the search term:')
    if st.button('Search'):
        search_results = search_book(search_term)
        if not search_results.empty:
            st.write(search_results)
            selected_book_index = st.selectbox('Select a book to edit:', search_results.index)
            selected_book = search_results.loc[selected_book_index]
            
            # Edit book details section
            st.subheader('Edit Book Details')
            updated_book_name = st.text_input('Book Name', value=selected_book['Book Name'])
            updated_author = st.text_input('Author', value=selected_book['Author'])
            updated_genre = st.text_input('Genre', value=selected_book['Genre'])
            updated_publication = st.text_input('Publication', value=selected_book['Publication'])
            updated_date_of_publication = st.date_input('Date of Publication', value=pd.to_datetime(selected_book['Date of Publication']))
            updated_isbn = st.text_input('ISBN Number', value=selected_book['ISBN'])
            updated_rack_number = st.text_input('Rack Number', value=selected_book['Rack Number'])
            updated_floor = st.text_input('Floor', value=selected_book['Floor'])
            
            if st.button('Update'):
                updated_data = {
                    'Book Name': updated_book_name,
                    'Author': updated_author,
                    'Genre': updated_genre,
                    'Publication': updated_publication,
                    'Date of Publication': updated_date_of_publication.strftime('%Y-%m-%d'),
                    'ISBN': updated_isbn,
                    'Rack Number': updated_rack_number,
                    'Floor': updated_floor
                }
                update_book(selected_book['Book Name'], updated_data)
                st.success('Book details updated successfully!')
        else:
            st.warning('No matching book found in the database.')

    # Add book section
    st.subheader('Add a Book')
    book_name = st.text_input('Book Name')
    author = st.text_input('Author')
    genre = st.text_input('Genre')
    publication = st.text_input('Publication')
    date_of_publication = st.date_input('Date of Publication', value=datetime.today())
    isbn = st.text_input('ISBN Number')
    rack_number = st.text_input('Rack Number')
    floor = st.text_input('Floor')
    
    if st.button('Submit'):
        if not all([book_name, author, genre, publication, isbn, rack_number, floor]):
            st.error("Please fill all required fields.")
        else:
            book_data = pd.DataFrame({
                'Book Name': [book_name],
                'Author': [author],
                'Genre': [genre],
                'Publication': [publication],
                'Date of Publication': [date_of_publication.strftime('%Y-%m-%d')],
                'ISBN': [isbn],
                'Rack Number': [rack_number],
                'Floor': [floor]
            })
            add_book(book_data)
            st.success('Book added successfully!')

if __name__ == '__main__':
    main()
