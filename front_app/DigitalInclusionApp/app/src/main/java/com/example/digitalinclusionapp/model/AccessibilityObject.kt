package com.example.digitalinclusionapp.model

import com.google.android.gms.maps.model.LatLng

data class AccessibilityObject(
    val id: Int,
    val name_ru: String?,
    val district_name: String?,
    val location: GeometryData?,
    val category_info: CategoryInfo?
)

data class GeometryData(
    val type: String,
    val coordinates: List<Double> // [Longitude, Latitude]
) {
    fun toLatLng(): LatLng = LatLng(coordinates[1], coordinates[0])
}

data class CategoryInfo(
    val name_ru: String?,
    val icon: String?,
    val color: String?
)