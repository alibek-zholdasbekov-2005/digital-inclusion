package com.example.digitalinclusionapp.activity

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.setupWithNavController
import com.example.digitalinclusionapp.R
import com.example.digitalinclusionapp.databinding.ActivityStoreBinding

class StoreActivity : AppCompatActivity() {
    private lateinit var binding: ActivityStoreBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityStoreBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Правильный способ поиска NavController для FragmentContainerView
        val navHostFragment = supportFragmentManager
            .findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        val navController = navHostFragment.navController

        // Связываем нижнее меню с навигацией
        binding.bottomNavigation.setupWithNavController(navController)
    }
}