from fastapi import FastAPI,Depends,HTTPException
from typing import List
import schemas,models
from sqlalchemy.orm import Session
from database import engine,SessionLocal
app=FastAPI()
models.Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
#create operation
@app.post('/blog')
def create_blog(newblog:schemas.Blog,db:Session=Depends(get_db)):
    blog_to_be_added_in_database=models.Blog(name=newblog.name,description=newblog.description)
    db.add(blog_to_be_added_in_database)
    db.commit()
    db.refresh(blog_to_be_added_in_database)
    return blog_to_be_added_in_database


# read operation
@app.get('/blog',response_model=List[schemas.ShowBlog]) # just because of response model we'll get only name and description of blog as in ShowBlog schema
def get_blog(db: Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs  

# read blog with particular id
@app.get('/blog/{id}',response_model=schemas.ShowBlog)
def get_specific_blog(id:int,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404,detail=f"blog with id {id} not found")
    return blog

# update the blog
@app.put('/blog/{id}')
def update_blog(id:int,updated_blog:schemas.Blog,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=404,detail=f"blog with id {id} not found")
    blog.update({'name':updated_blog.name,"description":updated_blog.description})
    db.commit()
    return "updated"

    


#delete blog of particular id
@app.delete('/blog/{id}')
def delete_blog(id,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"blog with id {id} not found")
    else:
        blog.delete(synchronize_session=False)
        db.commit() 
        return "deleted"