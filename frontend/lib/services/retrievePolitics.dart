//dart file that contains the function called RetrievePolitics that reads an entire json from a specific location

import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> retrievePolitics() async {
  final response =
      await http.get(Uri.parse('http://127.0.0.1:5000/summarized/politics'));

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Failed to load politics data');
  }
}
