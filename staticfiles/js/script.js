let currentIndex1 = 0;
        let currentIndex2 = 0;

        // Fonction pour déplacer le carrousel
        function moveCarousel(direction, carouselNumber) {
            let productList;
            let currentIndex;
            if (carouselNumber === 1) {
                productList = document.getElementById('productList1');
                currentIndex = currentIndex1;
            } else {
                productList = document.getElementById('productList2');
                currentIndex = currentIndex2;


            }

            const productWidth = document.querySelector('.product').offsetWidth + 20; // Espace entre les produits
            const totalProducts = document.querySelectorAll(`#productList${carouselNumber} .product`).length;

            if (direction === 1) {
                currentIndex--;
                if (currentIndex < 0) {
                    currentIndex = totalProducts - 1; // Revenir à la fin si au début
                }
            } else if (direction === -1) {
                currentIndex++;
                if (currentIndex >= totalProducts) {
                    currentIndex = 0; // Revenir au début si à la fin
                }
            }

            if (carouselNumber === 1) {
                currentIndex1 = currentIndex;
            } else {
                currentIndex2 = currentIndex;
            }

            const offset = -currentIndex * productWidth;
            productList.style.transform = `translateX(${offset}px)`;
        }

        // function addToCart() {
        //     alert('Produit ajouté au panier');
        // }

        function searchProduct() {
            const searchTerm = document.getElementById("searchInput").value;
            alert("Recherche pour : " + searchTerm);
        }

        function viewCart() {
            alert("Affichage du panier");
        }