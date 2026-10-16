import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:image_picker/image_picker.dart';
import 'package:marine_see/app.dart';
import 'package:marine_see/classify/classifier.dart';
import 'package:marine_see/classify/stub_classifier.dart';
import 'package:marine_see/screens/result_screen.dart';
import 'package:marine_see/theme/theme.dart';
import 'package:marine_see/theme/tokens.dart';

void main() {
  test('StubClassifier does not invent a species or confidence', () async {
    final result = await StubClassifier().identify(XFile('dummy.jpg'));
    expect(result.status, IdentifyStatus.stub);
    expect(result.slug, isNull);
    expect(result.confidence, isNull);
    expect(result.message, StubClassifier.notConnectedMessage);
  });

  testWidgets('tab screens fit a 375-wide phone', (tester) async {
    tester.view.physicalSize = const Size(375, 812);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const MarineSeeApp());
    await tester.pump();

    expect(find.text('Identify seagrass'), findsOneWidget);
    await tester.tap(find.text('Skip'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));

    expect(find.text('Welcome back,').hitTestable(), findsOneWidget);
    expect(find.text('Guest').hitTestable(), findsOneWidget);
    expect(find.text('Mati City').hitTestable(), findsOneWidget);
    expect(find.text('Scan Seagrass').hitTestable(), findsOneWidget);
    expect(find.text('Your Impact'), findsNothing);
    expect(find.textContaining('71%'), findsNothing);
    expect(find.text('CNN Model Active'), findsNothing);

    await tester.tap(find.byTooltip('Scan'));
    await tester.pump();
    expect(find.text('No photo yet').hitTestable(), findsOneWidget);
    expect(find.text('Camera').hitTestable(), findsOneWidget);
    expect(find.text('Gallery').hitTestable(), findsOneWidget);
    expect(find.text('Identify').hitTestable(), findsOneWidget);

    await tester.tap(find.byTooltip('Library'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(find.text('Showing 9 species').hitTestable(), findsOneWidget);
    expect(find.text('Cymodocea rotundata').hitTestable(), findsWidgets);

    await tester.tap(find.byTooltip('Conservation'));
    await tester.pump();
    expect(find.text('Why seagrass matters').hitTestable(), findsOneWidget);
    expect(find.text('TBD — adviser source').hitTestable(), findsOneWidget);

    await tester.tap(find.byTooltip('Profile'));
    await tester.pump();
    expect(
      find.text('MarineSee identifies and teaches the nine Mati species.').hitTestable(),
      findsOneWidget,
    );
    expect(find.text('Camera or gallery').hitTestable(), findsOneWidget);
  });

  testWidgets('identify error shows the error and Try again', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: buildMarineSeeTheme(AppTokens.sky),
        home: ResultScreen(
          imageBytes: _png,
          result: const IdentifyResult(
            status: IdentifyStatus.error,
            message: 'Cannot reach the identify API.',
          ),
        ),
      ),
    );
    await tester.pump();

    expect(find.text('Cannot reach the identify API.'), findsOneWidget);
    expect(find.text('Try again'), findsOneWidget);
    expect(find.text('Open species profile'), findsNothing);
    expect(find.text('Open 3D'), findsNothing);
    expect(find.textContaining('Cymodocea'), findsNothing);
  });

  testWidgets('a finished identify shows the name and percent', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: buildMarineSeeTheme(AppTokens.sky),
        home: ResultScreen(
          imageBytes: _png,
          result: const IdentifyResult(
            slug: 'enhalus_acoroides',
            confidence: 0.62,
            status: IdentifyStatus.ok,
          ),
        ),
      ),
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));

    expect(find.text('Enhalus acoroides'), findsOneWidget);
    expect(find.text('62%'), findsOneWidget);
    expect(find.text(ResultScreen.retakeSentence), findsNothing);
    expect(find.text('Open species profile'), findsOneWidget);
    await tester.scrollUntilVisible(find.text('Try again'), 200);
    expect(find.text('Open 3D'), findsOneWidget);
  });

  testWidgets('low confidence shows the name, percent, and retake notice', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: buildMarineSeeTheme(AppTokens.sky),
        home: ResultScreen(
          imageBytes: _png,
          result: const IdentifyResult(
            slug: 'cymodocea_rotundata',
            confidence: 0.42,
            status: IdentifyStatus.lowConfidence,
            message: ResultScreen.retakeSentence,
          ),
        ),
      ),
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));

    expect(find.text('Cymodocea rotundata'), findsOneWidget);
    expect(find.text('42%'), findsOneWidget);
    expect(find.text(ResultScreen.retakeSentence), findsOneWidget);
    expect(find.text('Open species profile'), findsOneWidget);
    await tester.scrollUntilVisible(find.text('Try again'), 200);
    expect(find.text('Open 3D'), findsOneWidget);
    expect(find.text('Try again'), findsOneWidget);
  });
}

final _png = base64Decode(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII=',
);
