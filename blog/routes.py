from flask import render_template, url_for, request, redirect, flash
from blog import app, db
from blog.models import User, Post, Comment, PostLike, PostTag
from blog.forms import RegistrationForm, LoginForm, CommentForm
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from sqlalchemy import or_, and_, func
from urllib.parse import urlparse, urljoin

@app.route("/")
@app.route("/home")
def home():
  com = []
  discusses = Comment.query.order_by(Comment.date.desc()).limit(3).all()
  for discuss in discusses:
    com.append(discuss.post_id)
  com = list(set(com))
  post = Post.query.filter(Post.id.in_(com)).all()
  c = [next(co for co in post if co.id ==id)for id in com]
  discusslist = postcount(c)
  list1 = []
  postLike = db.session.query(PostLike.post_id,func.count(1)).group_by(PostLike.post_id).order_by(func.count(1).desc())
  for postL in postLike:
    list1.append(postL.post_id)
  posts=Post.query.filter(Post.id.in_(list1)).all()
  l = [next(s for s in posts if s.id == id) for id in list1]
  postlist = postcount(l)
  return render_template('home.html',posts=postlist,discusses=discusslist)

@app.route("/allPosts/<int:sort>",methods=['GET'])
def allPosts(sort):
  print(sort)
  page = int(request.args.get('page', 1))
  if sort == 0:
    paginate = Post.query.order_by(Post.date).paginate(page, 2, False)
  elif sort==1:
    paginate = Post.query.order_by(Post.date.desc()).paginate(page, 2, False)
  else:
    paginate = Post.query.order_by(Post.date).paginate(page, 2, False)
  posts = paginate.items
  postlist = postcount(posts)
  return render_template('allPosts.html',paginate=paginate,posts=postlist,sort=sort)

@app.route("/about")
def about():
  return render_template('about.html', title='About')

@app.route("/popular")
def popular():
  com = []
  discusses = Comment.query.order_by(Comment.date.desc()).limit(3).all()
  for discuss in discusses:
    com.append(discuss.post_id)
  com = list(set(com))
  post = Post.query.filter(Post.id.in_(com)).all()
  c = [next(co for co in post if co.id ==id)for id in com]
  discusslist = postcount(c)
  list1 = []
  postLike = db.session.query(PostLike.post_id,func.count(1)).group_by(PostLike.post_id).order_by(func.count(1).desc())
  for postL in postLike:
    list1.append(postL.post_id)
  posts=Post.query.filter(Post.id.in_(list1)).all()
  l = [next(s for s in posts if s.id == id) for id in list1]
  postlist = postcount(l)
  return render_template('home.html',posts=postlist,discusses=discusslist)

@app.route("/newest")
def newest():
  com = []
  discusses = Comment.query.order_by(Comment.date.desc()).limit(3).all()
  for discuss in discusses:
    com.append(discuss.post_id)
  com = list(set(com))
  post = Post.query.filter(Post.id.in_(com)).all()
  c = [next(co for co in post if co.id ==id)for id in com]
  discusslist = postcount(c)
  posts=Post.query.order_by(Post.date.desc()).limit(10).all()
  postlist = postcount(posts)
  return render_template('home.html',posts=postlist,discusses=discusslist)

@app.route("/search")
def search():
  s = request.args.get('query')
  search = "%{}%".format(s)
  posts=Post.query.order_by(Post.date.desc()).filter(or_(Post.content.like(search),Post.title.like(search)))
  postlist = postcount(posts)
  return render_template('home.html', posts=postlist)

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method == 'POST':
    post = Post(title=request.form['title'],content=request.form['content'],author_id=request.form['author_id'],like='0',comment='0')
    db.session.add(post)
    db.session.commit()
    flash("Your post has been posted","success")
    return redirect(url_for('home'))
  return render_template('add.html')

@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  comments = Comment.query.filter(Comment.post_id==post.id)
  if current_user.is_authenticated:
    post_like = PostLike.query.filter(and_(PostLike.user_id==current_user.id,PostLike.post_id==post_id)).all()
    post_tag = PostTag.query.filter(and_(PostTag.user_id==current_user.id,PostTag.post_id==post_id)).all()
  else:
    post_like = []
    post_tag = []
  form = CommentForm()
  return render_template('post.html',post=post,comments=comments,postLike=post_like,tagLists=post_tag,postId=post_id,form=form,next=request.path)

@app.route('/post/<int:post_id>/comment',methods=['GET','POST'])
@login_required
def post_comment(post_id):
  post=Post.query.get_or_404(post_id)
  form=CommentForm()
  if form.validate_on_submit():
    db.session.add(Comment(content=form.comment.data,post_id=post.id,author_id=current_user.id))
    db.session.commit()
    flash("Your comment has been added to the post","success")
    return redirect(f'/post/{post.id}')
  comments=Comment.query.filter(Comment.post_id==post.id)
  return render_template('post.html',post=post,comments=comments,form=form)

@app.route("/register",methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data,firstname=form.firstname.data,lastname=form.lastname.data,email=form.email.data,password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful!')
    if request.args.get('next') == '/register' or request.args.get('next') == '/login':
      return redirect(url_for('home'))
    else:
      return redirect(request.args.get('next') or url_for('home'))
  return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    print(user)
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('Login successful!')
      if request.args.get('next') == '/login' or request.args.get('next') == '/register':
        return redirect(url_for('home'))
      else:
        return redirect(request.args.get('next') or url_for('home'))
    flash('Invalid email address or password.')
    return render_template('login.html',form=form)
  return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash('Logout successful!')
  return redirect(request.args.get('next') or url_for('home'))


@app.route('/post/<int:post_id>/like',methods=['POST'])
def like(post_id):
  if current_user.is_authenticated:
    post=Post.query.get_or_404(post_id)
    db.session.add(PostLike(post_id=post.id,user_id=current_user.id))
    db.session.commit()
    flash("Like successful","success")
    return redirect(f'/post/{post.id}')
  else:
    flash("Please login first")
    return redirect(url_for('login'))

@app.route('/post/<int:post_id>/unlike',methods=['POST'])
def unlike(post_id):
  if current_user.is_authenticated:
    post=Post.query.get_or_404(post_id)
    postLike = PostLike.query.filter(and_(PostLike.user_id==current_user.id,PostLike.post_id==post_id)).first()
    db.session.delete(postLike)
    db.session.commit()
    flash("unlike successful","success")
    return redirect(f'/post/{post.id}')
  else:
    flash("Please login first")
    return redirect(url_for('login'))

@app.route('/post/<int:post_id>/tag',methods=['POST'])
def tag(post_id):
  if current_user.is_authenticated:
    post=Post.query.get_or_404(post_id)
    db.session.add(PostTag(post_id=post.id,user_id=current_user.id))
    db.session.commit()
    flash("tag successful","success")
    return redirect(f'/post/{post.id}')
  else:
    flash("Please login first")
    return redirect(request.args.get('next') or url_for('login'))

@app.route('/post/<int:post_id>/untag',methods=['POST'])
def untag(post_id):
  if current_user.is_authenticated:
    post=Post.query.get_or_404(post_id)
    postTag = PostTag.query.filter(and_(PostTag.user_id==current_user.id,PostTag.post_id==post_id)).first()
    db.session.delete(postTag)
    db.session.commit()
    flash("untag successful","success")
    return redirect(f'/post/{post.id}')
  else:
    flash("Please login first")
    return redirect(url_for('login'))

@app.route("/tagList")
@login_required
def tagList():
  list1 = []
  tagLists=PostTag.query.filter(PostTag.user_id==current_user.id).all()
  for tagList in tagLists:
    list1.append(tagList.post_id)
  posts=Post.query.filter(Post.id.in_(list1)).all()
  for post in posts:
    count = PostLike.query.filter(PostLike.post_id==post.id).count()
    post.like = count
  return render_template('tagList.html',posts=posts)

@app.route("/removeTag/<int:post_id>")
@login_required
def removeTag(post_id):
  tag = PostTag.query.filter(and_(PostTag.user_id==current_user.id,PostTag.post_id==post_id)).first()
  db.session.delete(tag)
  db.session.commit()
  flash('success')
  return redirect(url_for('tagList'))

def redirect_back(backurl, **kwargs):
    for target in request.args.get('next'), request.referrer:
        print(target)
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(backurl, **kwargs))
 
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def postcount(postlist):
  for post in postlist:
    likecount = PostLike.query.filter(PostLike.post_id==post.id).count()
    commentcount = Comment.query.filter(Comment.post_id==post.id).count()
    post.like = likecount
    post.comment = commentcount
  return postlist

@app.errorhandler(401)
def page_not_found(e):
  print(e)
  return render_template('401.html'), 401