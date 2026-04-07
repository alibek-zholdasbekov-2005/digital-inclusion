package com.example.digitalinclusionapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent // Important!
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.example.digitalinclusionapp.ui.MainMapScreen
import com.example.digitalinclusionapp.ui.theme.DigitalInclusionAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Ensure NO 2GIS code is here!

        enableEdgeToEdge()
        setContent {
            DigitalInclusionAppTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    MainMapScreen()
                }
            }
        }
    }
}