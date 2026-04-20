package com.example.digitalinclusionapp.fragments

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.digitalinclusionapp.R
import com.example.digitalinclusionapp.api.RetrofitInstance
import com.example.digitalinclusionapp.databinding.FragmentHomeBinding
import com.example.digitalinclusionapp.model.AccessibilityObject
import com.example.digitalinclusionapp.repository.MapRepository
import com.example.digitalinclusionapp.viewmodel.MapViewModel
import com.example.digitalinclusionapp.viewmodel.MapViewModelFactory
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions

class HomeFragment : Fragment(R.layout.fragment_home), OnMapReadyCallback {
    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private lateinit var viewModel: MapViewModel
    private var googleMap: GoogleMap? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentHomeBinding.bind(view)
        binding.mapView.onCreate(savedInstanceState)
        binding.mapView.getMapAsync(this)

        val repository = MapRepository(RetrofitInstance.api)
        val factory = MapViewModelFactory(repository)
        viewModel = ViewModelProvider(this, factory).get(MapViewModel::class.java)

        observeData()
    }

    override fun onMapReady(map: GoogleMap) {
        googleMap = map
        val almaty = LatLng(43.2389, 76.8897)
        map.moveCamera(CameraUpdateFactory.newLatLngZoom(almaty, 12f))
        viewModel.fetchObjects()
    }

    private fun observeData() {
        viewModel.objects.observe(viewLifecycleOwner) { list ->
            googleMap?.clear()
            list?.forEach { obj ->
                obj.location?.let { geo ->
                    val pos = LatLng(geo.coordinates[1], geo.coordinates[0])
                    googleMap?.addMarker(MarkerOptions().position(pos).title(obj.name_ru))
                }
            }
        }
    }

    override fun onResume() { super.onResume(); binding.mapView.onResume() }
    override fun onPause() { super.onPause(); binding.mapView.onPause() }
    override fun onDestroyView() { super.onDestroyView(); _binding = null }
}