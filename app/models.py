
from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    # 1. General Information
    gender = Column(String, index=True)
    age = Column(Integer, index=True)
    educational_institution = Column(String, index=True)
    x = Column(Integer, index=True)
    y = Column(Integer, index=True)
    time = Column(Integer, index=True)



    # 2. Budget
    budget_mean = Column(Integer, index=True)  # Mu (средний)
    budget_deviation = Column(Integer, index=True)  # Sigma (разброс)

    # 3. Behavioral Scales (0-100)
    cleanliness = Column(Integer, index=True)
    sleep_time = Column(Integer, index=True)
    noise_tolerance = Column(Integer, index=True)
    hosting_frequency = Column(Integer, index=True)
    guest_tolerance = Column(Integer, index=True)
    smoking_attitude = Column(Integer, index=True)
    animal_tolerance = Column(Integer, index=True)
    sociability = Column(Integer, index=True)
    personal_space_need = Column(Integer, index=True)
    shared_purchases = Column(Integer, index=True)
    hobby_noise_level = Column(Integer, index=True)
    common_area_cleaning = Column(Integer, index=True)
    joint_activities_interest = Column(Integer, index=True)



    hashed_password = Column(String)