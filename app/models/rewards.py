from .db import db, environment, SCHEMA, add_prefix_for_prod


class Reward(db.Model):
    __tablename__ = "rewards"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("campaigns.id"))
    )
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    campaign = db.relationship("Campaign", back_populates="rewards")
    supports = db.relationship(
        "Support", back_populates="reward", cascade="all, delete-orphan"
    )

    def to_dict(self):
        supports_list = [support.supporter_id()["user_id"] for support in self.supports]
        supports_full_list = [support.to_dict() for support in self.supports]
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "campaign": self.campaign.name,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "supports": supports_list,
            "supports_full": supports_full_list,
        }
