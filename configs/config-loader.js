#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class ConfigLoader {
  constructor() {
    this.configsDir = path.join(__dirname, 'presets');
    this.cache = new Map();
  }

  getPresetsList() {
    const presetsFile = path.join(this.configsDir, 'presets.json');
    if (!fs.existsSync(presetsFile)) {
      return [];
    }
    const data = JSON.parse(fs.readFileSync(presetsFile, 'utf8'));
    return data.presets;
  }

  loadPreset(presetId) {
    if (this.cache.has(presetId)) {
      return this.cache.get(presetId);
    }

    const presets = this.getPresetsList();
    const preset = presets.find(p => p.id === presetId);

    if (!preset) {
      return null;
    }

    const presetFile = path.join(this.configsDir, preset.file);
    if (!fs.existsSync(presetFile)) {
      return null;
    }

    const config = JSON.parse(fs.readFileSync(presetFile, 'utf8'));
    this.cache.set(presetId, config);
    return config;
  }

  getDefaultPreset() {
    const presetsFile = path.join(this.configsDir, 'presets.json');
    if (!fs.existsSync(presetsFile)) {
      return null;
    }
    const data = JSON.parse(fs.readFileSync(presetsFile, 'utf8'));
    return this.loadPreset(data.defaultPreset);
  }

  loadUserConfig(userConfigPath) {
    if (!userConfigPath || !fs.existsSync(userConfigPath)) {
      return null;
    }
    return JSON.parse(fs.readFileSync(userConfigPath, 'utf8'));
  }

  mergeConfigs(presetConfig, userConfig) {
    if (!userConfig) return presetConfig;

    const merged = JSON.parse(JSON.stringify(presetConfig));

    function deepMerge(target, source) {
      for (const key in source) {
        if (source[key] instanceof Object && key in target) {
          deepMerge(target[key], source[key]);
        } else {
          target[key] = source[key];
        }
      }
    }

    deepMerge(merged, userConfig.config);
    return merged;
  }

  generateInteractiveOptions(type) {
    const optionsMap = {
      visualStyle: [
        { value: '国潮动漫风格', label: '国潮动漫', icon: '🎨' },
        { value: '日漫风格', label: '日漫风格', icon: '🎌' },
        { value: '皮克斯风格', label: '皮克斯风格', icon: '🏠' },
        { value: '真人写实风格', label: '真人写实', icon: '🎬' },
        { value: '迪士尼风格', label: '迪士尼风格', icon: '✨' },
        { value: '韩漫风格', label: '韩漫风格', icon: '💫' },
        { value: '赛博朋克风格', label: '赛博朋克', icon: '🤖' },
        { value: '3D CG风格', label: '3D CG', icon: '🎮' }
      ],
      targetMedium: [
        { value: '电影', label: '电影', icon: '🎬' },
        { value: '短剧', label: '短剧', icon: '📱' },
        { value: '漫剧', label: '漫剧', icon: '📖' },
        { value: 'MV', label: 'MV', icon: '🎵' },
        { value: '广告', label: '广告', icon: '📢' }
      ],
      aspectRatio: [
        { value: '16:9', label: '16:9 横屏', icon: '🖥️' },
        { value: '9:16', label: '9:16 竖屏', icon: '📱' },
        { value: '1:1', label: '1:1 方形', icon: '🟦' },
        { value: '2.35:1', label: '2.35:1 宽银幕', icon: '🎦' }
      ]
    };

    return optionsMap[type] || [];
  }
}

module.exports = ConfigLoader;

if (require.main === module) {
  const loader = new ConfigLoader();
  console.log('预设配置列表:');
  console.log(JSON.stringify(loader.getPresetsList(), null, 2));
}
