import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:image_picker/image_picker.dart';
import 'package:marine_see/app.dart';
import 'package:marine_see/classify/classifier.dart';
import 'package:marine_see/classify/stub_classifier.dart';

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
    await tester.pump(const Duration(milliseconds: 300));

    expect(find.text('No photo yet'), findsOneWidget);
    expect(find.byTooltip('Camera'), findsOneWidget);

    await tester.tap(find.byTooltip('Library'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(find.text('Cymodocea rotundata'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.menu));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(find.text('3D models'), findsOneWidget);
    expect(find.text('Profile'), findsOneWidget);

    await tester.tap(find.text('About'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(find.text('On this device'), findsOneWidget);
  });
}
