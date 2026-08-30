import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../classify/classifier.dart';
import '../theme/tokens.dart';
import 'result_screen.dart';

class IdentifyScreen extends StatefulWidget {
  const IdentifyScreen({super.key, required this.classifier});

  final Classifier classifier;

  @override
  State<IdentifyScreen> createState() => _IdentifyScreenState();
}

class _IdentifyScreenState extends State<IdentifyScreen> {
  final _picker = ImagePicker();
  File? _image;
  bool _busy = false;

  Future<void> _pick(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(source: source);
      if (picked == null) {
        return;
      }
      setState(() => _image = File(picked.path));
    } on PlatformException catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppTokens.danger,
          content: Text(
            error.message ?? 'Could not open the camera or gallery.',
            style: const TextStyle(color: AppTokens.onBrand),
          ),
        ),
      );
    }
  }

  Future<void> _identify() async {
    final image = _image;
    if (image == null || _busy) {
      return;
    }
    setState(() => _busy = true);
    final result = await widget.classifier.identify(image);
    if (!mounted) {
      return;
    }
    setState(() => _busy = false);
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ResultScreen(image: image, result: result),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Identify')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
        children: [
          Text(
            'Take a photo or choose one from the gallery. Then tap Identify.',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: AppTokens.ink,
            ),
          ),
          const SizedBox(height: 16),
          _Preview(image: _image),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => _pick(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera),
                  label: const Text('Camera'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => _pick(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library),
                  label: const Text('Gallery'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: _image == null || _busy ? null : _identify,
            child: Text(_busy ? 'Identifying…' : 'Identify'),
          ),
        ],
      ),
    );
  }
}

class _Preview extends StatelessWidget {
  const _Preview({required this.image});

  final File? image;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: SizedBox(
        height: 240,
        width: double.infinity,
        child: image == null
            ? Center(
                child: Text(
                  'No image yet',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppTokens.inkMuted,
                  ),
                ),
              )
            : ClipRRect(
                borderRadius: BorderRadius.circular(AppTokens.radius),
                child: Image.file(
                  image!,
                  fit: BoxFit.contain,
                  width: double.infinity,
                ),
              ),
      ),
    );
  }
}
