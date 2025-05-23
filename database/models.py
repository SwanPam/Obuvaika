import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func, UniqueConstraint
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Используемый Enum
class SizeType(enum.Enum):
    EU = "EU"
    US = "US"
    UK = "UK"
    CM = "CM"


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


# Справочные таблицы
class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class AgeCategory(Base):
    __tablename__ = "age_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Color(Base):
    __tablename__ = "colors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class UpperMaterial(Base):
    __tablename__ = "upper_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class LiningMaterial(Base):
    __tablename__ = "lining_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class Style(Base):
    __tablename__ = "styles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


# Основная таблица продукта
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    article: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    discount: Mapped[int] = mapped_column(Integer, default=0)

    product_category_id: Mapped[int] = mapped_column(ForeignKey("product_categories.id"), nullable=False)
    product_category: Mapped["ProductCategory"] = relationship()

    age_category_id: Mapped[int] = mapped_column(ForeignKey("age_categories.id"), nullable=False)
    age_category: Mapped["AgeCategory"] = relationship()

    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"), nullable=False)
    season: Mapped["Season"] = relationship()

    color_id: Mapped[int] = mapped_column(ForeignKey("colors.id"), nullable=False)
    color: Mapped["Color"] = relationship()

    upper_material_id: Mapped[int] = mapped_column(ForeignKey("upper_materials.id"), nullable=False)
    upper_material: Mapped["UpperMaterial"] = relationship()

    lining_material_id: Mapped[int] = mapped_column(ForeignKey("lining_materials.id"), nullable=False)
    lining_material: Mapped["LiningMaterial"] = relationship()

    last_width: Mapped[int] = mapped_column(Integer)

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    brand: Mapped["Brand"] = relationship()

    style_id: Mapped[int] = mapped_column(ForeignKey("styles.id"), nullable=False)
    style: Mapped["Style"] = relationship()

    heel_height: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    sizes: Mapped[List["ProductSize"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    images: Mapped[List["ProductImage"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    @property
    def final_price(self) -> int:
        return self.price * (100 - self.discount) // 100


# Размеры и связи
class Size(Base):
    __tablename__ = "sizes"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(10), nullable=False)
    type: Mapped[SizeType] = mapped_column(Enum(SizeType), nullable=False)

    __table_args__ = (
        UniqueConstraint("value", "type", name="uq_size_value_type"),
    )


class ProductSize(Base):
    __tablename__ = "product_sizes"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["Product"] = relationship(back_populates="sizes")
    size: Mapped["Size"] = relationship()


# Изображения
class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)
    order: Mapped[int] = mapped_column(Integer, default=0)

    product: Mapped["Product"] = relationship(back_populates="images")

# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)  # Внешний ID (например, Telegram ID)
#     username: Mapped[Optional[str]] = mapped_column(String(100))  # Имя пользователя (может быть None)
#     first_login: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())  # Время первого входа

