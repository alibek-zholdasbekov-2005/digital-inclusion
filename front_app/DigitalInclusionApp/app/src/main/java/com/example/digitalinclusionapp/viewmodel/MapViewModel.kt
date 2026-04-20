package com.example.digitalinclusionapp.viewmodel

import androidx.lifecycle.*
import com.example.digitalinclusionapp.model.AccessibilityObject
import com.example.digitalinclusionapp.repository.MapRepository
import kotlinx.coroutines.launch

class MapViewModel(private val repository: MapRepository) : ViewModel() {
    val objects = MutableLiveData<List<AccessibilityObject>>()
    val selectedObject = MutableLiveData<AccessibilityObject?>()
    val error = MutableLiveData<String>()

    fun fetchObjects() {
        viewModelScope.launch {
            try {
                val response = repository.getObjects()
                if (response.isSuccessful) {
                    objects.postValue(response.body())
                }
            } catch (e: Exception) {
                error.postValue("Ошибка загрузки данных")
            }
        }
    }

    fun selectObject(obj: AccessibilityObject) { selectedObject.value = obj }
    fun deselectObject() { selectedObject.value = null }
}

class MapViewModelFactory(private val repository: MapRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return MapViewModel(repository) as T
    }
}