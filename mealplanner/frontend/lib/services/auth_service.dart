import '../models/user.dart';
import 'api_client.dart';
import '../config/api_config.dart';

class AuthService {
  final ApiClient _client = ApiClient();

  Future<AuthToken> login(String email, String password) async {
    final response = await _client.post(
      ApiConfig.authLogin,
      body: {
        'username': email,
        'password': password,
      },
    );
    final token = AuthToken.fromJson(response as Map<String, dynamic>);
    await _client.setToken(token.accessToken);
    return token;
  }

  Future<User> register(String email, String password, String displayName) async {
    final response = await _client.post(
      ApiConfig.authRegister,
      body: {
        'email': email,
        'password': password,
        'display_name': displayName,
      },
    );
    return User.fromJson(response as Map<String, dynamic>);
  }

  Future<User> getProfile() async {
    final response = await _client.get(ApiConfig.usersMe);
    return User.fromJson(response as Map<String, dynamic>);
  }

  Future<User> updateProfile({
    String? displayName,
    String? preferredStoreId,
    Map<String, dynamic>? dietaryPreferences,
    int? householdSize,
  }) async {
    final body = <String, dynamic>{};
    if (displayName != null) body['display_name'] = displayName;
    if (preferredStoreId != null) body['preferred_store_id'] = preferredStoreId;
    if (dietaryPreferences != null) body['dietary_preferences'] = dietaryPreferences;
    if (householdSize != null) body['household_size'] = householdSize;

    final response = await _client.put(ApiConfig.usersMe, body: body);
    return User.fromJson(response as Map<String, dynamic>);
  }

  Future<void> updateAllergens(List<String> allergenIds) async {
    await _client.put(ApiConfig.usersAllergens, body: {'allergen_ids': allergenIds});
  }

  Future<void> logout() async {
    await _client.clearToken();
  }
}
