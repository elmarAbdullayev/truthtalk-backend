from app.core.database import Base, engine
from app.models import user, room, participant

print("Creating tables...")
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")