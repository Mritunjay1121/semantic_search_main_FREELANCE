import streamlit as st
from embed_and_store_data import final
def main():
    st.title("Search For the Query")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = final(search_query)

            # Display search results
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['Series_Title']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Overview: {result['_source']['Overview_new']}")
                        except Exception as e:
                            print(e)


                        try:
                            st.write(f"Score: {result['_score']}")
                        except Exception as e:
                            print(e)


                            
                        st.divider()


if __name__ == "__main__":
    main()
