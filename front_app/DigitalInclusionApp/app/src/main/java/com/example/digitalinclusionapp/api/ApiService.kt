package com.example.digitalinclusionapp.api

import com.example.digitalinclusionapp.model.*
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @POST("api/register/")
    suspend fun register(@Body request: RegisterRequest): Response<Unit>

    @POST("api/token/")
    suspend fun loginUser(@Body request: Map<String, String>): Response<TokenResponse>

    @GET("api/objects/")
    suspend fun getObjects(): Response<List<AccessibilityObject>>
}