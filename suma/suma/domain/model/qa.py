from dataclasses import dataclass

# models


@dataclass
class UserProfile:
    display_name: str


@dataclass
class Post:
    user_profile: UserProfile
    title: str
    body: str
    type: str


# repositories
