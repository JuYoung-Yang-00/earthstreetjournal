//import 'dart:ui';

import 'package:flutter/material.dart';

import 'dart:math' as math;
import 'dart:async';
import 'dart:ui';

import 'package:url_launcher/url_launcher.dart';

import 'package:flutter_animate/flutter_animate.dart';

//import 'dart:ui' as ui;

class CategoryHeader extends StatefulWidget {
  const CategoryHeader(
      {super.key,
      required this.title,
      required this.selected,
      required this.goesTo});

  final String title;
  final bool selected;
  final Widget goesTo;

  @override
  State<CategoryHeader> createState() => _CategoryHeaderState();
}

class _CategoryHeaderState extends State<CategoryHeader> {
  bool isHovered = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: MouseRegion(
        onEnter: (_) {
          setState(() {
            isHovered = true;
          });
        },
        onExit: (_) {
          setState(() {
            isHovered = false;
          });
        },
        child: InkWell(
          onTap: () async {
            // i might have to do await 200 milliseconds
            Navigator.of(context).push(PageRouteBuilder(
              pageBuilder: (context, animation, secondaryAnimation) =>
                  widget.goesTo,
              transitionsBuilder:
                  (context, animation, secondaryAnimation, child) {
                // This is just a fade transition, but you can customize as needed.
                return FadeTransition(opacity: animation, child: child);
              },
            ));
          },
          splashColor: Colors.transparent,
          highlightColor: Colors.transparent,
          hoverColor: Colors.transparent,
          child: Animate(
            effects: const [
              FadeEffect(duration: Duration(seconds: 1)),
            ],
            child: Text(
              widget.title,
              style: TextStyle(
                fontFamily: widget.selected ? 'Thonburi-Bold' : 'Thonburi',
                fontSize: widget.selected ? 15 : 14,
                color: isHovered
                    ? const Color(0xff00684b)
                    : widget.selected
                        ? const Color(0xff00684b)
                        : const Color(0xff272C32),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
