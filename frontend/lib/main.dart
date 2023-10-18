import 'package:flutter/material.dart';
import './landingPage.dart';

import 'package:flutter_web_plugins/flutter_web_plugins.dart';

import 'package:go_router/go_router.dart';

void main() {
  runApp(MyApp());
  setUrlStrategy(PathUrlStrategy());
}

final GoRouter _router = GoRouter(
  initialLocation: '/',
  routes: <RouteBase>[
    GoRoute(
      path: '/',
      builder: (BuildContext context, GoRouterState state) {
        return const LandingPage(title: 'Earth Street Journal');
      },
      routes: <RouteBase>[
        /*
        GoRoute(
          path: 'artists',
          builder: (BuildContext context, GoRouterState state) {
            return const ArtistsPage(title: 'artists');
          },
        ),
        */
      ],
    ),
  ],
);

class MyApp extends StatelessWidget {
  MyApp({super.key});

  // Define your custom theme here
  final ThemeData customTheme = ThemeData(
    primaryColor: const Color(0xFFFAFAFA), // #FAFAFA in hexadecimal
    scaffoldBackgroundColor: const Color(0xFFF9F7F2), // #202123 in hexadecimal
    // You can define other theme properties here as well
  );

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
      theme: customTheme, // Apply the custom theme here
    );
  }
}
