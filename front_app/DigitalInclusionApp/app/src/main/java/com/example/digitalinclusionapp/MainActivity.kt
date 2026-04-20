package com.example.digitalinclusionapp

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.asLiveData
import com.example.digitalinclusionapp.activity.LoginActivity
import com.example.digitalinclusionapp.activity.StoreActivity
import com.example.digitalinclusionapp.util.TokenManager

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val tokenManager = TokenManager(this)

        // Проверка токена: если есть — на главный экран, если нет — на логин
        tokenManager.getToken().asLiveData().observe(this) { token ->
            if (!token.isNullOrEmpty()) {
                startActivity(Intent(this, StoreActivity::class.java))
            } else {
                startActivity(Intent(this, LoginActivity::class.java))
            }
            finish()
        }
    }
}