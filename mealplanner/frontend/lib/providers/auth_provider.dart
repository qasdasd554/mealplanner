import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../services/api_client.dart';

class AuthProvider with ChangeNotifier {
  final AuthService _authService = AuthService();
  final ApiClient _apiClient = ApiClient();

  User? _currentUser;
  bool _isAuthenticated = false;
  bool _isLoading = false;
  String? _errorMessage;

  User? get currentUser => _currentUser;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  AuthProvider() {
    _checkTokenOnInit();
  }

  Future<void> _checkTokenOnInit() async {
    final token = await _apiClient.getToken();
    if (token != null) {
      _isAuthenticated = true;
      notifyListeners();
      await loadProfile();
    }
  }

  Future<bool> login(String email, String password) async {
    _setLoading(true);
    _clearError();
    try {
      await _authService.login(email, password);
      _isAuthenticated = true;
      notifyListeners();
      await loadProfile();
      _setLoading(false);
      return true;
    } catch (e) {
      _setErrorMessage(e.toString().replaceAll('ApiException: ', ''));
      _setLoading(false);
      return false;
    }
  }

  Future<bool> register(String email, String password, String displayName) async {
    _setLoading(true);
    _clearError();
    try {
      await _authService.register(email, password, displayName);
      // Auto login po rejestracji
      final success = await login(email, password);
      _setLoading(false);
      return success;
    } catch (e) {
      _setErrorMessage(e.toString().replaceAll('ApiException: ', ''));
      _setLoading(false);
      return false;
    }
  }

  Future<void> loadProfile() async {
    try {
      _currentUser = await _authService.getProfile();
      notifyListeners();
    } catch (e) {
      // Jeśli profil nie załaduje się prawidłowo (np. wygasł token), wyloguj
      await logout();
    }
  }

  Future<bool> updateProfile({
    String? displayName,
    String? preferredStoreId,
    Map<String, dynamic>? dietaryPreferences,
    int? householdSize,
  }) async {
    _clearError();
    try {
      final updatedUser = await _authService.updateProfile(
        displayName: displayName,
        preferredStoreId: preferredStoreId,
        dietaryPreferences: dietaryPreferences,
        householdSize: householdSize,
      );
      _currentUser = updatedUser;
      notifyListeners();
      return true;
    } catch (e) {
      _setErrorMessage(e.toString().replaceAll('ApiException: ', ''));
      return false;
    }
  }

  Future<bool> saveOnboardingPreferences({
    required String storeId,
    required List<String> allergenIds,
    required String diet,
    required int householdSize,
  }) async {
    _setLoading(true);
    try {
      // 1. Zapisz profil (sklep, dieta, household)
      await updateProfile(
        preferredStoreId: storeId,
        dietaryPreferences: {'diet': diet},
        householdSize: householdSize,
      );
      // 2. Zapisz alergeny
      await _authService.updateAllergens(allergenIds);
      await loadProfile();
      _setLoading(false);
      return true;
    } catch (e) {
      _setErrorMessage(e.toString().replaceAll('ApiException: ', ''));
      _setLoading(false);
      return false;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    _currentUser = null;
    _isAuthenticated = false;
    notifyListeners();
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }

  void _setErrorMessage(String msg) {
    _errorMessage = msg;
    notifyListeners();
  }

  void _clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}
