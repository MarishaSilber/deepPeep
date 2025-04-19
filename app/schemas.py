from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# User Authentication Models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# User Preferences Models
class UserPreferencesBase(BaseModel):
    # 1. General Information
    gender: str = Field(..., example="мужской", description="Пол: мужской/женский/другое")
    age: int = Field(..., ge=18, le=99, example=22, description="Возраст (18-99)")
    educational_institution: str = Field(..., example="МГУ", description="Название учебного заведения")
    max_walking_minutes: int = Field(..., ge=5, le=60, example=15,
                                     description="Максимальное время пешком до вуза (5-60 минут)")

    # 2. Budget
    budget_mean: int = Field(..., gt=0, example=30000, description="Средний желаемый бюджет (в рублях)")
    budget_deviation: int = Field(..., gt=0, example=5000, description="Допустимое отклонение бюджета (в рублях)")

    # 3. Behavioral Scales (0-100)
    cleanliness: int = Field(..., ge=0, le=100, example=80, description="Уровень чистоплотности (0-100)")
    sleep_time: int = Field(..., ge=0, le=100, example=60, description="Предпочитаемое время сна (0-100)")
    noise_tolerance: int = Field(..., ge=0, le=100, example=50, description="Толерантность к шуму (0-100)")
    hosting_frequency: int = Field(..., ge=0, le=100, example=30, description="Частота приглашения гостей (0-100)")
    guest_tolerance: int = Field(..., ge=0, le=100, example=70, description="Терпимость к гостям соседа (0-100)")
    smoking_attitude: int = Field(..., ge=0, le=100, example=20, description="Отношение к курению (0-100)")
    animal_tolerance: int = Field(..., ge=0, le=100, example=60, description="Терпимость к животным (0-100)")
    sociability: int = Field(..., ge=0, le=100, example=50, description="Уровень общительности (0-100)")
    personal_space_need: int = Field(..., ge=0, le=100, example=60,
                                     description="Потребность в личном пространстве (0-100)")
    shared_purchases: int = Field(..., ge=0, le=100, example=40, description="Отношение к совместным покупкам (0-100)")
    hobby_noise_level: int = Field(..., ge=0, le=100, example=30, description="Шумность хобби (0-100)")
    common_area_cleaning: int = Field(..., ge=0, le=100, example=70, description="Частота уборки общих зон (0-100)")
    joint_activities_interest: int = Field(..., ge=0, le=100, example=50,
                                           description="Интерес к совместным активностям (0-100)")


class UserPreferencesCreate(UserPreferencesBase):
    pass


class UserPreferences(UserPreferencesBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Combined User Response Model
class UserWithPreferences(User):
    preferences: Optional[UserPreferences] = None