import 'package:flutter/foundation.dart';

class ApiConfig {
  // Dynamiczne dopasowanie adresu URL w zależności od platformy
  static String get baseUrl {
    if (kIsWeb) {
      final uri = Uri.base;
      // Jeśli działamy w GitHub Codespaces (web)
      if (uri.host.contains('app.github.dev')) {
        // Zamieniamy końcowy numer portu w subdomenie Codespaces na -8000 (backend)
        final newHost = uri.host.replaceFirst(RegExp(r'-\d+(?=\.app\.github\.dev$)'), '-8000');
        return '${uri.scheme}://$newHost';
      }
      // Jeśli to lokalny serwer webowy na komputerze
      if (uri.host == 'localhost' || uri.host == '127.0.0.1') {
        return 'http://localhost:8000';
      }
    }
    // Domyślnie dla emulatora Androida
    return 'http://10.0.2.2:8000';
  }

  static const String apiPrefix = '/api/v1';

  static String get apiUrl => '$baseUrl$apiPrefix';

  // Endpointy
  static const String authLogin = '/auth/login';
  static const String authRegister = '/auth/register';
  static const String usersMe = '/users/me';
  static const String usersAllergens = '/users/me/allergens';
  static const String stores = '/stores/';
  static const String products = '/products/';
  static const String recipes = '/recipes/';
  static const String recipesAvailable = '/recipes/available';
  static const String mealPlans = '/meal-plans/';
  static const String shoppingLists = '/shopping-lists/';
}
