from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Recipe, Comment
from app.classes.forms import RecipeForm, CommentForm
from flask_login import login_required
import datetime as dt
from app.classes.data import Recipe, Comment



@app.route('/recipes')
@app.route('/recipe/list')
@login_required
def recipeList():

    recipes = Recipe.objects()

    return render_template('recipes.html',recipes=recipes)


@app.route('/recipe/<recipeID>')
@login_required
def recipe(recipeID):
    thisRecipe = Recipe.objects.get(id=recipeID)
    theseComments = Comment.objects(recipe=thisRecipe)
    return render_template('recipe.html',recipe=thisRecipe,comments=theseComments)

@app.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def recipeNew():
    form = RecipeForm()
    if form.validate_on_submit():
        newRecipe = Recipe(
            name = form.name.data,
            genre = form.genre.data,
            recauthor = form.recauthor.data,
            author = current_user.id,
            summary = form.summary.data,
            ingredients = form.ingredients.data,
            time = form.time.data,
            recrecipe = form.recrecipe.data,
            tags = form.tags.data,
            create_date = dt.datetime.utcnow,
            modify_date = dt.datetime.utcnow
        )
        newRecipe.save()
        if form.recimage.data:
            newRecipe.recimage.put(form.recimage.data, content_type = 'image/jpeg')
            # This saves all the updates
            newRecipe.save()
        return redirect(url_for('recipe',recipeID=newRecipe.id))
    return render_template('recipeform.html',form=form)


@app.route('/recipe/delete/<recipeID>')

@login_required
def recipeDelete(recipeID):
   
    deleteRecipe = Recipe.objects.get(id=recipeID)
    if current_user == deleteRecipe.author:
    
        deleteRecipe.delete()
    
        flash('The Recipe was deleted.')
    else:
        flash("You can't delete a recipe you don't own.")

    recipes = Recipe.objects()  
    return render_template('recipe.html',recipes=recipes)

@app.route('/recipe/edit/<recipeID>', methods=['GET', 'POST'])
@login_required
def recipeEdit(recipeID):
    editrecipe = Recipe.objects.get(id=recipeID)
    if current_user != editrecipe.author:
        flash("You can't edit a recipe you don't own.")
        return redirect(url_for('recipe',recipeID=recipeID))

    form = RecipeForm()
      
    if form.validate_on_submit():
        editrecipe.update(
            name = form.name.data,
            genre = form.genre.data,
            recauthor = form.recauthor.data,
            author = current_user.id,
            summary = form.summary.data,
            ingredients = form.ingredients.data,
            time = form.time.data,
            recrecipe = form.recrecipe.data,
            tags = form.tags.data,
            modify_date = dt.datetime.utcnow
        )
        if form.recimage.data:
            if editrecipe.recimage:
                editrecipe.recimage.delete()
            editrecipe.recimage.put(form.recimage.data, content_type = 'image/jpeg')
            # This saves all the updates
            editrecipe.save()
    
        return redirect(url_for('recipe',recipeID=recipeID))


    form.name.data = editrecipe.name
    form.genre.data = editrecipe.genre
    form.recauthor.data = editrecipe.recauthor
    form.summary.data = editrecipe.summary
    form.ingredients.data = editrecipe.ingredients
    form.time.data = editrecipe.time
    form.recrecipe.data = editrecipe.recrecipe
    form.tags.data = editrecipe.tags
    

    return render_template('recipeform.html',form=form, recipe=recipe)


@app.route('/comment/new/<recipeID>', methods=['GET', 'POST'])
@login_required
def commentNew(recipeID):
    recipe = Recipe.objects.get(id=recipeID)
    form = CommentForm()
    if form.validate_on_submit():
        newComment = Comment(
            author = current_user.id,
            recipe = recipeID,
            content = form.content.data
        )
        newComment.save()
        return redirect(url_for('recipe',recipeID=recipeID))
    return render_template('commentform.html',form=form,recipe=recipe)

@app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def commentEdit(commentID):
    editComment = Comment.objects.get(id=commentID)
    if current_user != editComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('recipe',recipeID=editComment.recipe.id))
    recipe = Recipe.objects.get(id=editComment.recipe.id)
    form = CommentForm()
    if form.validate_on_submit():
        editComment.update(
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('recipe',recipeID=editComment.recipe.id))

    form.content.data = editComment.content

    return render_template('commentform.html',form=form,recipe=recipe)   

@app.route('/comment/delete/<commentID>')
@login_required
def commentDelete(commentID): 
    deleteComment = Comment.objects.get(id=commentID)
    deleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('recipe',recipeID=deleteComment.recipe.id)) 


