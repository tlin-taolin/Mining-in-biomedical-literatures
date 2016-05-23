
package org.dmg.pmml;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import org.dmg.pmml.adapters.DecimalAdapter;
import org.dmg.pmml.adapters.IntegerAdapter;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element ref="{http://www.dmg.org/PMML-4_2}Extension" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://www.dmg.org/PMML-4_2}ItemRef" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="id" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="support" type="{http://www.dmg.org/PMML-4_2}PROB-NUMBER" />
 *       &lt;attribute name="numberOfItems" type="{http://www.w3.org/2001/XMLSchema}nonNegativeInteger" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "extensions",
    "itemRefs"
})
@XmlRootElement(name = "Itemset", namespace = "http://www.dmg.org/PMML-4_2")
public class Itemset
    extends PMMLObject
    implements HasExtensions, HasId
{

    @XmlAttribute(name = "id", required = true)
    protected String id;
    @XmlAttribute(name = "support")
    @XmlJavaTypeAdapter(DecimalAdapter.class)
    protected Double support;
    @XmlAttribute(name = "numberOfItems")
    @XmlJavaTypeAdapter(IntegerAdapter.class)
    @XmlSchemaType(name = "nonNegativeInteger")
    protected Integer numberOfItems;
    @XmlElement(name = "Extension", namespace = "http://www.dmg.org/PMML-4_2")
    protected List<Extension> extensions;
    @XmlElement(name = "ItemRef", namespace = "http://www.dmg.org/PMML-4_2")
    protected List<ItemRef> itemRefs;

    public Itemset() {
        super();
    }

    public Itemset(final String id) {
        super();
        this.id = id;
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    /**
     * Gets the value of the support property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public Double getSupport() {
        return support;
    }

    /**
     * Sets the value of the support property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSupport(Double value) {
        this.support = value;
    }

    /**
     * Gets the value of the numberOfItems property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public Integer getNumberOfItems() {
        return numberOfItems;
    }

    /**
     * Sets the value of the numberOfItems property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setNumberOfItems(Integer value) {
        this.numberOfItems = value;
    }

    /**
     * Gets the value of the extensions property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the extensions property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getExtensions().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Extension }
     * 
     * 
     */
    public List<Extension> getExtensions() {
        if (extensions == null) {
            extensions = new ArrayList<Extension>();
        }
        return this.extensions;
    }

    /**
     * Gets the value of the itemRefs property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the itemRefs property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getItemRefs().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link ItemRef }
     * 
     * 
     */
    public List<ItemRef> getItemRefs() {
        if (itemRefs == null) {
            itemRefs = new ArrayList<ItemRef>();
        }
        return this.itemRefs;
    }

    public Itemset withId(String value) {
        setId(value);
        return this;
    }

    public Itemset withSupport(Double value) {
        setSupport(value);
        return this;
    }

    public Itemset withNumberOfItems(Integer value) {
        setNumberOfItems(value);
        return this;
    }

    public Itemset withExtensions(Extension... values) {
        if (values!= null) {
            for (Extension value: values) {
                getExtensions().add(value);
            }
        }
        return this;
    }

    public Itemset withExtensions(Collection<Extension> values) {
        if (values!= null) {
            getExtensions().addAll(values);
        }
        return this;
    }

    public Itemset withItemRefs(ItemRef... values) {
        if (values!= null) {
            for (ItemRef value: values) {
                getItemRefs().add(value);
            }
        }
        return this;
    }

    public Itemset withItemRefs(Collection<ItemRef> values) {
        if (values!= null) {
            getItemRefs().addAll(values);
        }
        return this;
    }

    public boolean hasExtensions() {
        return ((this.extensions!= null)&&(this.extensions.size()> 0));
    }

    public boolean hasItemRefs() {
        return ((this.itemRefs!= null)&&(this.itemRefs.size()> 0));
    }

    @Override
    public VisitorAction accept(Visitor visitor) {
        VisitorAction status = visitor.visit(this);
        visitor.pushParent(this);
        for (int i = 0; (((status == VisitorAction.CONTINUE)&&(this.extensions!= null))&&(i<this.extensions.size())); i ++) {
            status = this.extensions.get(i).accept(visitor);
        }
        for (int i = 0; (((status == VisitorAction.CONTINUE)&&(this.itemRefs!= null))&&(i<this.itemRefs.size())); i ++) {
            status = this.itemRefs.get(i).accept(visitor);
        }
        visitor.popParent();
        if (status == VisitorAction.TERMINATE) {
            return VisitorAction.TERMINATE;
        }
        return VisitorAction.CONTINUE;
    }

}
