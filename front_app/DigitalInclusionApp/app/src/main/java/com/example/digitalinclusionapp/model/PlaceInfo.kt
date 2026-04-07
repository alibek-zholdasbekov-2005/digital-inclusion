package com.example.digitalinclusionapp.model

data class PlaceInfo(
    val name: String,
    val category: String,
    val rating: Float,
    val reviewCount: Int,
    val address: String,
    val phone: String,
    val accessibilityDescription: String, // Updated name
    val accessibilityStatus: String       // Updated name
)