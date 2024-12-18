import { defineStore } from 'pinia'
const images = import.meta.glob('@/assets/img/products/*.png*', { eager: true })

// Преобразуем объект `images` в объект с путями
const resolvedImages = Object.fromEntries(
  Object.entries(images).map(([key, value]) => [key, value.default]),
)
console.log(resolvedImages)

export const useGoodsStore = defineStore('goods', {
  state: () => ({
    goods: [
      {
        id: 1,
        title: 'Устрицы по рокфеллеровски',
        description:
          'Свежайшие устрицы, запечённые под сливочным соусом с зеленью и сыром. Блюдо для истинных гурманов, которое подается с ломтиками лимона.',
        price: 2700,
        imageSource: resolvedImages['/src/assets/img/products/image0.png'],
      },
      {
        id: 2,
        title: 'Свиные ребрышки на гриле с зеленью',
        description:
          'Сочные свиные ребрышки, приготовленные на гриле, подаются с ароматной зеленью и чесночным соусом. Идеальный выбор для любителей мяса.',
        price: 1600,
        imageSource: resolvedImages['/src/assets/img/products/image1.png'],
      },
      {
        id: 3,
        title: 'Креветки по-королевски в лимонном соке',
        description:
          'Крупные креветки, замаринованные в свежем лимонном соке и приготовленные до идеальной текстуры. Подаются с соусом из пряных трав.',
        price: 1820,
        imageSource: resolvedImages['/src/assets/img/products/image2.png'],
      },
      {
        id: 4,
        title: 'Мидии в белом вине с чесноком',
        description:
          'Мидии, приготовленные в белом вине с добавлением чеснока, петрушки и сливочного масла. Блюдо обладает утончённым вкусом и ароматом моря.',
        price: 2200,
        imageSource: resolvedImages['/src/assets/img/products/image3.png'],
      },
      {
        id: 5,
        title: 'Стейк рибай с соусом чимичурри',
        description:
          'Мраморный стейк рибай, приготовленный до желаемой степени прожарки. Подается с пикантным соусом чимичурри, на основе свежей зелени, чеснока и оливкового масла.',
        price: 3500,
        imageSource: resolvedImages['/src/assets/img/products/image4.png'],
      },
      {
        id: 6,
        title: 'Каре ягнёнка с розмарином',
        description:
          'Нежное каре ягнёнка, обжаренное до золотистой корочки и приправленное свежим розмарином. Подается с соусом на основе красного вина.',
        price: 3800,
        imageSource: resolvedImages['/src/assets/img/products/image5.png'],
      },
      {
        id: 7,
        title: 'Сашими из лосося',
        description:
          'Тонкие ломтики свежего лосося, нарезанные вручную. Подаются с соевым соусом, васаби и маринованным имбирем для утончённого вкусового удовольствия.',
        price: 2400,
        imageSource: resolvedImages['/src/assets/img/products/image6.png'],
      },
      {
        id: 8,
        title: 'Том ям с морепродуктами',
        description:
          'Классический тайский суп с креветками, мидиями, грибами и ароматными специями. Пикантный вкус усиливается соком лайма и кокосовым молоком.',
        price: 1500,
        imageSource: resolvedImages['/src/assets/img/products/image7.png'],
      },
      {
        id: 9,
        title: 'Цезарь с креветками',
        description:
          'Классический салат с хрустящими листьями ромена, золотистыми креветками, домашними гренками и пармезаном, заправленный оригинальным соусом Цезарь.',
        price: 1300,
        imageSource: resolvedImages['/src/assets/img/products/image8.png'],
      },
      {
        id: 10,
        title: 'Тартар из тунца с авокадо',
        description:
          'Свежий тунец мелко нарезан и подан с кубиками спелого авокадо. Завершает блюдо пикантный соус терияки и кунжутные семена.',
        price: 2100,
        imageSource: resolvedImages['/src/assets/img/products/image9.png'],
      },
      {
        id: 11,
        title: 'Гребешки на гриле с лимоном',
        description:
          'Морские гребешки, обжаренные на гриле до золотистой корочки, подаются с ломтиками лимона и свежими травами. Настоящий деликатес.',
        price: 3200,
        imageSource: resolvedImages['/src/assets/img/products/image10.png'],
      },
      {
        id: 12,
        title: 'Дорада с ароматными травами',
        description:
          'Свежая дорада, запечённая с тимьяном, розмарином и лимоном. Блюдо отличается нежным вкусом и утончённым ароматом.',
        price: 2900,
        imageSource: resolvedImages['/src/assets/img/products/image11.png'],
      },
      {
        id: 13,
        title: 'Филе лосося на пару с соусом юдзу',
        description:
          'Лосось, приготовленный на пару для сохранения всех полезных свойств, подаётся с освежающим соусом из японского цитруса юдзу.',
        price: 3100,
        imageSource: resolvedImages['/src/assets/img/products/image12.png'],
      },
      {
        id: 14,
        title: 'Паста с мидиями и креветками',
        description:
          'Домашняя паста, приготовленная со сливочно-чесночным соусом, украшенная мидиями и креветками. Завершает вкус тёртый пармезан.',
        price: 1800,
        imageSource: resolvedImages['/src/assets/img/products/image13.png'],
      },
      {
        id: 15,
        title: 'Рататуй с овощами',
        description:
          'Традиционное французское блюдо из свежих овощей, запечённых с травами Прованса. Яркий вкус и аппетитный аромат.',
        price: 1100,
        imageSource: resolvedImages['/src/assets/img/products/image14.png'],
      },
      {
        id: 16,
        title: 'Стейк из тунца с кунжутом',
        description:
          'Нежное филе тунца, обжаренное в кунжутной панировке. Подаётся с пикантным соусом терияки для усиления вкусовых акцентов.',
        price: 3500,
        imageSource: resolvedImages['/src/assets/img/products/image15.png'],
      },
    ],
    Product: null,
  }),
  getters: {
    getGoods: (state) => state.goods,
    getGoodById: (state) => (id) => state.goods.find((good) => good.id === id),
    getProductItem: (state) => state.Product,
  },
  actions: {
    setProductItem(val) {
      this.Product = this.goods.find((element) => element.id === Number(val))
    },
  },
})
