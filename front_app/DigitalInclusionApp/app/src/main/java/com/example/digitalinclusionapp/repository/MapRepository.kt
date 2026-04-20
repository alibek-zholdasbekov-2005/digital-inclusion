package com.example.digitalinclusionapp.repository

import com.example.digitalinclusionapp.api.ApiService

class MapRepository(private val api: ApiService) {
    suspend fun getObjects() = api.getObjects()
}