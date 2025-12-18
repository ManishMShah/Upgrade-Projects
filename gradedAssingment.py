# Supress Warnings
import warnings
warnings.filterwarnings('ignore')

# Import the numpy and pandas packages
import numpy as np
import pandas as pd

# Task 1: Reading and Inspection

# Subtask 1.1: Import and read
# Import and read the movie database. Store it in a variable called movies.
movies = pd.read_csv('Movie+Assignment+Data.csv')
print("Initial DataFrame:")
print(movies)

# Subtask 1.2: Inspect the dataframe
# Inspect the dataframe's columns, shapes, variable types etc.
print("\nDataFrame Info:")
print(movies.info())
print("\nDataFrame Head:")
print(movies.head())

# Task 2: Cleaning the Data

# Subtask 2.1: Inspect Null values
# Find out the number of Null values in all the columns and rows. Also, find the percentage of Null values in each column. Round off the percentages upto two decimal places.
print("\nColumn-wise null counts:")
print(movies.isnull().sum())
print("\nRow-wise null counts:")
print(movies.isnull().sum(axis=1))
print("\nColumn-wise null percentages:")
print(round((movies.isnull().sum() / len(movies.index)) * 100, 2))

# Subtask 2.2: Drop unecessary columns
# For this assignment, you will mostly be analyzing the movies with respect to the ratings, gross collection, popularity of movies, etc. So many of the columns in this dataframe are not required. So it is advised to drop the following columns.
columns_to_drop = [
    'color', 'director_facebook_likes', 'actor_1_facebook_likes',
    'actor_2_facebook_likes', 'actor_3_facebook_likes', 'actor_2_name',
    'cast_total_facebook_likes', 'actor_3_name', 'duration',
    'facenumber_in_poster', 'content_rating', 'country',
    'movie_imdb_link', 'aspect_ratio', 'plot_keywords'
]
movies.drop(columns=columns_to_drop, inplace=True)
print("\nDataFrame after dropping columns:")
print(movies.head())

# Subtask 2.3: Drop unecessary rows using columns with high Null percentages
# Now, on inspection you might notice that some columns have large percentage (greater than 5%) of Null values. Drop all the rows which have Null values for such columns.
columns_with_high_nulls = ['gross', 'budget']
movies.dropna(subset=columns_with_high_nulls, inplace=True)
print("\nDataFrame after dropping rows with high null percentages:")
print(movies.isnull().sum())

# Subtask 2.4: Drop unecessary rows
# Some of the rows might have greater than five NaN values. Such rows aren't of much use for the analysis and hence, should be removed.
movies.dropna(thresh=len(movies.columns) - 5, inplace=True)
print("\nDataFrame after dropping rows with more than 5 NaN values:")
print(movies.isnull().sum(axis=1))

# Subtask 2.5: Fill NaN values
# You might notice that the language column has some NaN values. Here, on inspection, you will see that it is safe to replace all the missing values with 'English'.
movies['language'].fillna('English', inplace=True)
print("\nDataFrame after filling NaN values in 'language' column:")
print(movies.isnull().sum())

# Subtask 2.6: Check the number of retained rows
# You might notice that two of the columns viz. num_critic_for_reviews and actor_1_name have small percentages of NaN values left. You can let these columns as it is for now. Check the number and percentage of the rows retained after completing all the tasks above.
original_rows = 5043
retained_rows = len(movies.index)
percentage_retained = (retained_rows / original_rows) * 100
print(f"\nNumber of retained rows: {retained_rows}")
print(f"Percentage of retained rows: {percentage_retained:.2f}%")

# Task 3: Data Analysis

# Subtask 3.1: Change the unit of columns
# Convert the unit of the budget and gross columns from $ to million $.
movies['budget'] = movies['budget'] / 1000000
movies['gross'] = movies['gross'] / 1000000
print("\nDataFrame after converting 'budget' and 'gross' to million $:")
print(movies[['budget', 'gross']].head())

# Subtask 3.2: Find the movies with highest profit
# 1. Create a new column called profit which contains the difference of the two columns: gross and budget.
movies['profit'] = movies['gross'] - movies['budget']
print("\nDataFrame with 'profit' column:")
print(movies[['gross', 'budget', 'profit']].head())

# 2. Sort the dataframe using the profit column as reference.
movies_sorted_by_profit = movies.sort_values(by='profit', ascending=False)
print("\nDataFrame sorted by profit:")
print(movies_sorted_by_profit[['movie_title', 'profit']].head())

# 3. Extract the top ten profiting movies in descending order and store them in a new dataframe - top10
top10 = movies_sorted_by_profit.head(10)
print("\nTop 10 profiting movies:")
print(top10[['movie_title', 'profit']])

# Subtask 3.3: Drop duplicate values
# After you found out the top 10 profiting movies, you might have notice a duplicate value. So, it seems like the dataframe has duplicate values as well. Drop the duplicate values from the dataframe and repeat Subtask 3.2.
movies.drop_duplicates(subset=['movie_title'], inplace=True)
print("\nDataFrame after dropping duplicates:")
print(movies.duplicated(subset=['movie_title']).sum())

# Repeat Subtask 3.2
movies['profit'] = movies['gross'] - movies['budget']
movies_sorted_by_profit_no_duplicates = movies.sort_values(by='profit', ascending=False)
top10_no_duplicates = movies_sorted_by_profit_no_duplicates.head(10)
print("\nTop 10 profiting movies after dropping duplicates:")
print(top10_no_duplicates[['movie_title', 'profit']])

# Subtask 3.4: Find IMDb Top 250
# 1. Create a new dataframe IMDb_Top_250 and store the top 250 movies with the highest IMDb Rating (corresponding to the column: imdb_score). Also make sure that for all of these movies, the num_voted_users is greater than 25,000.
IMDb_Top_250 = movies[movies['num_voted_users'] > 25000].sort_values(by='imdb_score', ascending=False).head(250)
IMDb_Top_250['Rank'] = range(1, len(IMDb_Top_250) + 1)
print("\nIMDb Top 250 movies:")
print(IMDb_Top_250[['movie_title', 'imdb_score', 'Rank']].head())

# 2. Extract all the movies in the IMDb_Top_250 dataframe which are not in the English language and store them in a new dataframe named Top_Foreign_Lang_Film.
Top_Foreign_Lang_Film = IMDb_Top_250[IMDb_Top_250['language'] != 'English']
print("\nTop foreign language films from IMDb Top 250:")
print(Top_Foreign_Lang_Film[['movie_title', 'language', 'imdb_score']])

# Subtask 3.5: Find the best directors
# 1. Group the dataframe using the director_name column.
# 2. Find out the top 10 directors for whom the mean of imdb_score is the highest and store them in a new dataframe top10director.
top10director = movies.groupby('director_name')['imdb_score'].mean().sort_values(ascending=False).head(10).to_frame()
print("\nTop 10 directors by average IMDb score:")
print(top10director)

# Subtask 3.6: Find popular genres
# 1. Extract the first two genres from the genres column and store them in two new columns: genre_1 and genre_2. Some of the movies might have only one genre. In such cases, extract the single genre into both the columns, i.e. for such movies the genre_2 will be the same as genre_1.
genres_split = movies['genres'].str.split('|', n=1, expand=True)
movies['genre_1'] = genres_split[0]
movies['genre_2'] = genres_split[1].fillna(movies['genre_1'])
print("\nDataFrame with 'genre_1' and 'genre_2' columns:")
print(movies[['genres', 'genre_1', 'genre_2']].head())

# 2. Group the dataframe using genre_1 as the primary column and genre_2 as the secondary column.
movies_by_segment = movies.groupby(['genre_1', 'genre_2'])

# 3. Find out the 5 most popular combo of genres by finding the mean of the gross values using the gross column and store them in a new dataframe named PopGenre.
PopGenre = movies_by_segment['gross'].mean().sort_values(ascending=False).head(5).to_frame()
print("\n5 most popular genre combos by mean gross:")
print(PopGenre)

# Subtask 3.7: Find the critic-favorite and audience-favorite actors
# 1. Create three new dataframes namely, Meryl_Streep, Leo_Caprio, and Brad_Pitt which contain the movies in which the actors: 'Meryl Streep', 'Leonardo DiCaprio', and 'Brad Pitt' are the lead actors. Use only the actor_1_name column for extraction. Also, make sure that you use the names 'Meryl Streep', 'Leonardo DiCaprio', and 'Brad Pitt' for the said extraction.
Meryl_Streep = movies[movies['actor_1_name'] == 'Meryl Streep']
Leo_Caprio = movies[movies['actor_1_name'] == 'Leonardo DiCaprio']
Brad_Pitt = movies[movies['actor_1_name'] == 'Brad Pitt']
print("\nMeryl Streep movies:")
print(Meryl_Streep[['movie_title', 'actor_1_name']].head())
print("\nLeonardo DiCaprio movies:")
print(Leo_Caprio[['movie_title', 'actor_1_name']].head())
print("\nBrad Pitt movies:")
print(Brad_Pitt[['movie_title', 'actor_1_name']].head())

# 2. Append the rows of all these dataframes and store them in a new dataframe named Combined.
Combined = pd.concat([Meryl_Streep, Leo_Caprio, Brad_Pitt])
print("\nCombined dataframe:")
print(Combined[['movie_title', 'actor_1_name']].head())

# 3. Group the combined dataframe using the actor_1_name column.
grouped_by_actor = Combined.groupby('actor_1_name')

# 4. Find the mean of the num_critic_for_reviews and num_user_for_review and identify the actors which have the highest mean.
critic_reviews_mean = grouped_by_actor['num_critic_for_reviews'].mean().sort_values(ascending=False)
user_reviews_mean = grouped_by_actor['num_user_for_reviews'].mean().sort_values(ascending=False)
print("\nMean critic reviews by actor:")
print(critic_reviews_mean)
print("\nMean user reviews by actor:")
print(user_reviews_mean)