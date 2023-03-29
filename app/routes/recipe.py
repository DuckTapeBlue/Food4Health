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
            genre = form.name.data,
            recauthor = form.recauthor.data,
            recimage = form.recimage.data,
            summary = form.summary.data,
            ingredients = form.ingredients.data,
            recrecipe = form.recrecipe.data,
            tags = form.tags.data,
            
            modify_date = dt.datetime.utcnow
        )

        newRecipe.save()
        return redirect(url_for('recipe',recipeID=newRecipe.id))
    return render_template('recipeform.html',form=form)



@app.route('/recipe/edit/<recipeID>', methods=['GET', 'POST'])
@login_required
def recipeEdit(recipeID):
    editrecipe = recipe.objects.get(id=recipeID)
    if current_user != editrecipe.author:
        flash("You can't edit a recipe you don't own.")
        return redirect(url_for('recipe',recipeID=recipeID))

    form = RecipeForm()

    if form.validate_on_submit():
        editrecipe.update(
            name = form.name.data,
            genre = form.name.data,
            recauthor = form.recauthor.data,
            recimage = form.recimage.data,
            summary = form.summary.data,
            ingredients = form.ingredients.data,
            recrecipe = form.recrecipe.data,
            tags = form.tags.data,
            modify_date = dt.datetime.utcnow
        )
    
        return redirect(url_for('recipe',recipeID=recipeID))

    form.subject.data = editrecipe.subject
    form.content.data = editrecipe.content
    form.tag.data = editrecipe.tag


  
    return render_template('recipeform.html',form=form)


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


