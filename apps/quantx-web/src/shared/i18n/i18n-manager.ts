export const LOCALE_CONFIG = {
  default: 'en-US',
  supported: ['en-US', 'ar-SA'],
  fallback: 'en-US',
};

export const LOCALES = {
  'en-US': {
    code: 'en-US',
    dir: 'ltr',
    name: 'English',
    dateFormat: 'MM/dd/yyyy',
    numberFormat: {
      decimal: '.',
      thousands: ',',
    },
  },
  'ar-SA': {
    code: 'ar-SA',
    dir: 'rtl',
    name: 'العربية',
    dateFormat: 'dd/MM/yyyy',
    numberFormat: {
      decimal: ',',
      thousands: '.',
    },
  },
};

export type LocaleCode = keyof typeof LOCALES;

class I18nManager {
  private currentLocale: LocaleCode;
  private translations: Record<string, Record<string, string>> = {};

  constructor() {
    this.currentLocale = this.detectLocale();
    this.loadTranslations();
  }

  private detectLocale(): LocaleCode {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('locale') as LocaleCode | null;
      if (saved && LOCALE_CONFIG.supported.includes(saved)) {
        return saved;
      }

      const browserLocale = navigator.language as LocaleCode;
      if (LOCALE_CONFIG.supported.includes(browserLocale)) {
        return browserLocale;
      }
    }

    if (LOCALE_CONFIG.supported.includes(LOCALE_CONFIG.default as LocaleCode)) {
      return LOCALE_CONFIG.default as LocaleCode;
    }
    return 'en-US';
  }

  private loadTranslations(): void {
    Object.keys(LOCALES).forEach((locale) => {
      this.translations[locale] = this.loadLocaleTranslations(locale);
    });
  }

  private loadLocaleTranslations(locale: string): Record<string, string> {
    const common = {
      'common.loading': locale === 'ar-SA' ? 'جاري التحميل...' : 'Loading...',
      'common.error': locale === 'ar-SA' ? 'خطأ' : 'Error',
      'common.retry': locale === 'ar-SA' ? 'إعادة المحاولة' : 'Retry',
      'common.save': locale === 'ar-SA' ? 'حفظ' : 'Save',
      'common.cancel': locale === 'ar-SA' ? 'إلغاء' : 'Cancel',
      'common.confirm': locale === 'ar-SA' ? 'تأكيد' : 'Confirm',
      'navigation.market': locale === 'ar-SA' ? 'السوق' : 'Market',
      'navigation.signals': locale === 'ar-SA' ? 'الإشارات' : 'Signals',
      'navigation.portfolio': locale === 'ar-SA' ? 'المحفظة' : 'Portfolio',
      'navigation.risk': locale === 'ar-SA' ? 'المخاطر' : 'Risk',
      'navigation.sharia': locale === 'ar-SA' ? 'الشريعة' : 'Sharia',
    };
    return common;
  }

  t(key: string, params?: Record<string, string>): string {
    let translation = this.translations[this.currentLocale]?.[key];
    
    if (!translation) {
      translation = this.translations[LOCALE_CONFIG.fallback]?.[key];
    }

    if (!translation && this.currentLocale !== LOCALE_CONFIG.fallback) {
      translation = key;
    }

    if (params && translation) {
      Object.entries(params).forEach(([param, value]) => {
        translation = translation!.replace(`{{${param}}}`, value);
      });
    }

    return translation || key;
  }

  formatCurrency(value: number, locale?: LocaleCode): string {
    const localeCode = locale || this.currentLocale;
    return new Intl.NumberFormat(localeCode, {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  }

  formatDate(date: Date | string, locale?: LocaleCode): string {
    const localeCode = locale || this.currentLocale;
    return new Intl.DateTimeFormat(localeCode).format(new Date(date));
  }

  formatNumber(value: number, locale?: LocaleCode): string {
    const localeCode = locale || this.currentLocale;
    return new Intl.NumberFormat(localeCode).format(value);
  }

  setLocale(locale: LocaleCode): void {
    if (LOCALE_CONFIG.supported.includes(locale)) {
      this.currentLocale = locale;
      if (typeof window !== 'undefined') {
        localStorage.setItem('locale', locale);
      }
      document.documentElement.dir = LOCALES[locale].dir;
      document.documentElement.lang = locale;
    }
  }

  getLocale(): LocaleCode {
    return this.currentLocale;
  }

  isRTL(): boolean {
    return LOCALES[this.currentLocale].dir === 'rtl';
  }
}

export const i18n = new I18nManager();