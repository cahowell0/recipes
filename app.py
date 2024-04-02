import os
import pickle
import tkinter
import customtkinter
import utils
import recipe_crawler as rc
from user_class import User
#this is fior fun
#download function
def startDownload(recipes_list):
    try:
        recipe_link = link.get()
        # recipeObject = 

        # Check website validity and permissions
        web_address = 'https://www.justonecookbook.com'
        html_file = 'recipes_list.html'
        url_file = 'recipe_links.p'
        pickle_recipes = 'pickle_recipes_file.p'
        all_recipes = web_address + '/tags/under-30-minutes/'


        if not os.path.exists(html_file):
            # Get crawl permissions        
            rc.check_valid_website(link, robots=True)

            # Check if website urls valid
            rc.check_valid_website(link)

        names_list = []   # Will hold names of recipes with punctuation / capitals removed
        url_list = []   # Will hold urls of all recipes

        # Scrape urls for all recipes, or load urls if previously scraped
        if not os.path.exists(url_file):
            while True:
                # Get urls for all recipes
                print('Retrieving recipe urls')
                urls, all_recipes = rc.get_url_list(all_recipes, html_file, names_list, crawl_delay=0.25)
                url_list.extend(urls)

                if all_recipes is None:
                    break

            # Save urls as pickle file for quick access
            with open(url_file, 'wb') as outfile:
                pickle.dump(url_list, outfile)

        else:
            # If we've already found the urls, load them in as list
            with open(url_file, 'rb') as infile:
                url_list = pickle.load(infile)


        # Scrape all recipes, or load if already scraped
        if not os.path.exists(pickle_recipes):
            # Scrape each url
            print('Scraping recipes')
            i = 0
            for url in url_list:
                on_progress(url_list, i)
                if i % 10 == 0:
                    print(i)
                new_recipe = rc.scrape_recipes(url, html_file, names_list, crawl_delay=0.25)
                if new_recipe is not None:
                    recipe_list.append(new_recipe)
                i += 1
                
            with open(pickle_recipes, 'wb') as outfile:
                pickle.dump(recipe_list, outfile)

        else:
            with open(pickle_recipes, 'rb') as infile:
                recipe_list = pickle.load(infile)
        print('Loaded recipes')

    except:
        print('Something bad happened')

#progress bar
def on_progress(url_list, i):
    total_size = len(url_list)
    progressBar.set(i / total_size)
    percentage_of_completion = i / total_size
    per = str(int(percentage_of_completion))
    progress_percent = customtkinter.CTkLabel(app, text='0%')
    progress_percent.pack(padx=10, pady=10)
    progress_percent.configure(text=per + '%')
    progress_percent.update()
    

#Ingredient options function
def noGo_ingredients():
    dislike_options = [[index] for index in dislikes_listbox.curselection()]
    print("Select ingredients you do not like:", dislike_options)

#Find any allergies
def allergy_finder():
    allergy_options = [allergies[index] for index in allergies_listbox.curselection()]
    other_value = other_entry.get()
    print("Select any alergies you may have: ", allergy_options)
    print("Input here for other: ", other_value)

#Score options funtion
def recipe_score():
    score_option = score.get()
    print("What would you rate this recipe?:", score_option)

#Save options function for dislikes
def save_selection():
    selected_indices = dislikes_listbox.curselection()
    selected_items = [dislikes_listbox.get(index) for index in selected_indices]
    print("Selected items:", selected_items)


def dislike_items_selected(event):
    pass

def create_user():
    new_user = User(unique_ingredients, userName.get(), recipe_list)
    print('hi')
    print(new_user.user_id)
    
    #TODO: Change allergy ingredients to 0

    
customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('blue')

app = customtkinter.CTk()
app.geometry('1920x1080')
app.title('Food app')

title = customtkinter.CTkLabel(app, text='Recipe', font=('arial', 36))
title.pack(padx=10, pady=50)


#get url
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, placeholder_text='Import recipes')
link.pack()

#download the url
recipe_list = []   # List to hold all Recipe objects
download = customtkinter.CTkButton(app, text = "Download", command=startDownload)
download.pack(padx=10,pady=10)

unique_ingredients = utils.get_unique_ingredients(recipe_list)

#download progress bar
# progress_percent = customtkinter.CTkLabel(app, text='0%')
# progress_percent.pack(padx=10, pady=10)

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)




# TODO: "Create a profile for a user"
name = tkinter.StringVar()
userName = customtkinter.CTkEntry(app, placeholder_text='What is your name?')
name_button = tkinter.Button(app, text = "Enter", command=create_user)
userName.bind()
userName.pack()
name_button.pack()

print('username', userName)


# TODO: "Have them input preferences, likes and dislikes to help initialize their taste"
dislikes_listbox = tkinter.Listbox(app, selectmode=tkinter.MULTIPLE)
dislike_var = tkinter.StringVar(app)
dislikes = ["Tomatos", "Fish", "Mayo", "Cilantro", "Pickles"]
dislike_var.set(dislikes)
for option in dislikes:
    dislikes_listbox.insert(tkinter.END, option)
dislike_button = tkinter.Button(app, text="Enter", command=noGo_ingredients)
dislikes_listbox.bind('<<ListboxSelect>>', dislike_items_selected)
dislikes_listbox.pack(pady=20)
dislike_button.pack()

#Check for allergies
allergies_listbox = tkinter.Listbox(app, selectmode=tkinter.MULTIPLE)
allergy = tkinter.StringVar(app)
allergies = ["Peanuts", "Gluten", "Milk", "Eggs", "Shellfish"]
allergy.set(allergies[0])
for option in allergies:
    allergies_listbox.insert(tkinter.END, option)
other_entry = customtkinter.CTkEntry(app, placeholder_text = "Other")
allergy_button = tkinter.Button(app, text="Enter", command=allergy_finder)
allergies_listbox.pack(pady=10)
other_entry.pack(pady=5)
allergy_button.pack(pady=10)
# TODO: "Recommend the first recipe (most popular)"

# TODO: "They input a score"
score = tkinter.StringVar(app)
scoreOptions = [str(i) for i in range(1, 6)]
score.set(scoreOptions[0])
score_menu = tkinter.OptionMenu(app, score, *scoreOptions)
score_button = tkinter.Button(app, text="Display Scores", command=recipe_score)
score_menu.pack(pady=20)
score_button.pack()
# TODO:"Run our algorithm"

# TODO: "Next recipe"



while app.mainloop():
   
    # TODO: "Next recipe"

    # TODO:"Run our algorithm"

    # TODO: "They input a score"

    pass
