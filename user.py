# Import necessary libraries
import streamlit as st
import pandas as pd

# Function to search for books by any information
def search_books_by_info(search_term):
    df = pd.read_excel('library_database.xlsx')
    result = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
    return result

# Main function for the search page
def search_page():
    st.title('Search Books')
    
    # Input search term
    search_term = st.text_input('Enter any information about the book:')
    
    # Search button
    if st.button('Search'):
        search_results = search_books_by_info(search_term)
        if not search_results.empty:
            st.subheader('Search Results:')
            st.write(search_results)
        else:
            st.warning('No matching books found.')

# Main function to run the Streamlit app
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ('Home', 'Search Books'))

    if page == 'Home':
        st.title('Library Management System')
        st.write('Welcome to the Library Management System!')
        
        st.header('Features:')
        st.markdown('- **Add Books:** Add new books to the library database.')
        st.markdown('- **Search Books:** Search for books using any information.')
        st.markdown('- **Edit Books:** Edit book details and update the database.')
        st.markdown('- **View Books:** View all books in the library.')
        
        st.header('Instructions:')
        st.markdown('1. Click on **Search Books** in the sidebar to search for books using any information.')
        st.markdown('2. Use the **Add a Book** section to add new books to the library.')
        st.markdown('3. After adding books, you can edit their details or view the entire library.')
        st.markdown('4. Have fun managing your library!')
        
    elif page == 'Search Books':
        search_page()

if __name__ == '__main__':
    main()
