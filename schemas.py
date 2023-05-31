from pydantic import BaseModel
class Blog(BaseModel):
    name: str
    description: str
class ShowBlog(BaseModel):
    id:int
    name:str #we want to show only id and name of blogs so we are using this schema class in showing blog
    
    class Config():
        orm_mode=True